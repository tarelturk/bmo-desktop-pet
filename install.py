#!/usr/bin/env python3
"""Install or restore the locally prepared BMO animation fix. Requires root."""
from pathlib import Path
import hashlib,os,sys,shutil,tempfile
ORIGINAL='5e5e186b50fe970b45744fd7bdf288980862af2d01c588d12dd509fb3c794c8a'
PATCHED='4b847804f408c69fa4fc5897fa47c14272c7486204c40b364d66455446efac02'
PREVIOUS='864a5f1fdc17e9a054daebd90f20652d52211a1bd286e0ce87b982e3f9c8271f'
target=Path('/usr/lib/chatgpt/resources/app.asar')
backup=target.with_name('app.asar.before-bmo-fix')
source=Path(__file__).resolve().parent/'app.asar.bmo-fixed'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def require(ok,message):
 if not ok:sys.exit(message)
def atomic_copy(src,dest):
 fd,name=tempfile.mkstemp(prefix='.bmo-',dir=dest.parent);os.close(fd)
 try:
  shutil.copyfile(src,name);os.chmod(name,0o644)
  with open(name,'rb') as f:os.fsync(f.fileno())
  require(sha(Path(name))==sha(src),'Kopya doğrulanamadı; değişiklik yapılmadı.')
  os.replace(name,dest)
 finally:
  if os.path.exists(name):os.unlink(name)
mode=sys.argv[1] if len(sys.argv)>1 else 'install'
require(mode in ('install','restore','check'),'Kullanım: install.py [install|restore|check]')
require(target.is_file(),'ChatGPT uygulama dosyası bulunamadı.')
current=sha(target)
if mode=='check':
 require(sha(source)==PATCHED,'Hazırlanan dosya doğrulanamadı.')
 require(current in (ORIGINAL,PREVIOUS,PATCHED),'Uygulama sürümü değişmiş; bu düzeltmeyi kurmayın.')
 print('Dosyalar doğrulandı. '+('Düzeltme kurulu.' if current==PATCHED else 'Düzeltme kuruluma hazır.'));sys.exit()
require(os.geteuid()==0,'Kurulum için bu dosyayı sudo python3 ile çalıştırın.')
if mode=='restore':
 require(current==PATCHED,'Uygulama değişmiş; otomatik geri alma durduruldu.')
 require(backup.is_file() and sha(backup)==ORIGINAL,'Orijinal yedek doğrulanamadı.')
 atomic_copy(backup,target);print('Orijinal sürüm geri yüklendi. ChatGPT uygulamasını tamamen kapatıp açın.');sys.exit()
if current==PATCHED:print('Düzeltme zaten kurulu. ChatGPT uygulamasını tamamen kapatıp açın.');sys.exit()
require(current in (ORIGINAL,PREVIOUS),'Uygulama sürümü değişmiş; güvenlik için kurulum durduruldu.')
require(sha(source)==PATCHED,'Hazırlanan dosya doğrulanamadı.')
if backup.exists():require(sha(backup)==ORIGINAL,'Mevcut yedek farklı; üzerine yazılmadı.')
else:
 require(current==ORIGINAL,'Orijinal yedek bulunamadı; kurulum durduruldu.')
 atomic_copy(target,backup)
atomic_copy(source,target)
print('BMO animasyon düzeltmesi kuruldu ve orijinal dosya yedeklendi. ChatGPT uygulamasını tamamen kapatıp yeniden açın.')
