from pathlib import Path
import json,struct,hashlib,copy
src=Path('/usr/lib/chatgpt/resources/app.asar.before-bmo-fix')
if not src.is_file(): raise SystemExit('Original backup missing; install the stock ChatGPT app first.')
if hashlib.sha256(src.read_bytes()).hexdigest() != '5e5e186b50fe970b45744fd7bdf288980862af2d01c588d12dd509fb3c794c8a': raise SystemExit('Unsupported ChatGPT build; stopping safely.')
out=Path('build');out.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
with src.open('rb') as f:
 prefix=f.read(16);raw=f.read(struct.unpack('<I',prefix[12:])[0]);header=json.loads(raw);base=8+struct.unpack('<I',prefix[4:8])[0]
 def entries(d,p=''):
  for k,v in d.items():
   path=p+'/'+k
   if 'files'in v:yield from entries(v['files'],path)
   elif 'offset'in v:yield path,v
 files=sorted(entries(header['files']),key=lambda x:int(x[1]['offset']))
 changes={}
 def replace(s,a,b):
  assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
 for path,v in files:
  name=path.rsplit('/',1)[-1]
  if name not in ['app-initial-e8b2527a6d62.js','avatar-mascot-button-e36577fa74ae.js','main-UOTY8NmV.js','avatar-overlay-native-page-387d903c4492.js']:continue
  f.seek(base+int(v['offset']));data=f.read(v['size']);assert sha(data)==v['integrity']['hash'];s=data.decode()
  if name.startswith('app-initial'):
   s=replace(s,'if(n)return{frames:r,loopStartIndex:0};','if(n||e===`running`)return{frames:r,loopStartIndex:0};')
   s=replace(s,'running:ZZ(7,6,120,220)','running:ZZ(7,6,120,120)')
   s=replace(s,'rea=nea.map(e=>({...e,frameDurationMs:e.frameDurationMs*tea}))','rea=nea.map((e,i)=>({...e,frameDurationMs:i===0?2600:i===5?1000:e.frameDurationMs}))')
   # While gazing, periodically blink using existing idle artwork; clean up on gaze/state change.
   s=replace(s,'if(n!=null){e.style.backgroundPosition=$9i(n,p);return}', 'if(n!=null){let a=[],o=()=>{e.style.backgroundPosition=$9i(n,p)};o();if(!d){let s=()=>{a.push(window.setTimeout(()=>{[1,2,3,4].forEach((t,r)=>a.push(window.setTimeout(()=>{e.style.backgroundPosition=$9i(nea[t],p)},r*85)));a.push(window.setTimeout(()=>{o();a=[];s()},340))},3400))};s()}return()=>{a.forEach(window.clearTimeout)}}')
  elif name.startswith('avatar-mascot'):
   s=replace(s,'p=f===`idle`||f===`running`||f===`waving`','p=f===`idle`')
  elif name.startswith('avatar-overlay'):
   s=replace(s,'rr=(Pn&&ft&&Vt?pn:null)??g?.caretPoint??dn','rr=dn??(Pn&&ft&&Vt?pn:null)??g?.caretPoint')
  else:
   # Poll only this pet window, only while visible, and do not override real computer-use events.
   marker='this.rendererReady=!0,this.pendingQuickChatFocus!=null'
   inject='this.rendererReady=!0,this.startBmoMouseTracking(t),this.pendingQuickChatFocus!=null'
   s=replace(s,marker,inject)
   method='''startBmoMouseTracking(e){if(this.isNotchManager)return;clearInterval(this.bmoGazeTimer);let last=null;this.bmoGazeTimer=setInterval(()=>{if(e.isDestroyed()){clearInterval(this.bmoGazeTimer);this.bmoGazeTimer=null;return}if(this.isSuspended||!e.isVisible()||!this.rendererReady||this.dragState!=null||this.computerUseCursorPoint!=null){last=null;return}try{let p=k.screen.getCursorScreenPoint(),b=e.getContentBounds(),point={x:p.x-b.x,y:p.y-b.y};if(last&&last.x===point.x&&last.y===point.y)return;last=point;this.windowManager.sendMessageToWebContents(e.webContents,{type:`avatar-overlay-computer-use-cursor-changed`,point})}catch{}},80);this.bmoGazeTimer.unref?.()}'''
   s=replace(s,'handleRendererReady(e){let t=this.window;',method+'handleRendererReady(e){let t=this.window;')
   s=replace(s,'t.on(`closed`,()=>{if(this.window!==t)return;this.stopObservingOutsideClicks?.()','t.on(`closed`,()=>{if(this.window!==t)return;clearInterval(this.bmoGazeTimer),this.bmoGazeTimer=null,this.stopObservingOutsideClicks?.()')
  changes[path]=s.encode();(Path('work/pet-runtime')/('v2-'+name)).write_text(s)
 # Preserve all file contents, update offsets and integrity for changed files.
 oldpositions={p:(int(v['offset']),v['size']) for p,v in files};offset=0
 for p,v in files:
  v['offset']=str(offset)
  if p in changes:
   data=changes[p];v['size']=len(data);it=v['integrity'];bs=it['blockSize'];it['hash']=sha(data);it['blocks']=[sha(data[i:i+bs]) for i in range(0,len(data),bs)]
  offset+=v['size']
 raw=json.dumps(header,separators=(',',':'),ensure_ascii=False).encode();payload=struct.pack('<I',len(raw))+raw;payload+=b'\0'*((-len(payload))%4);hp=struct.pack('<I',len(payload))+payload
 with (out/'app.asar.bmo-fixed').open('wb') as dest:
  dest.write(struct.pack('<II',4,len(hp))+hp)
  for p,v in files:
   if p in changes:dest.write(changes[p])
   else:
    pos,size=oldpositions[p];f.seek(base+pos)
    while size:
     b=f.read(min(size,4194304));assert b;dest.write(b);size-=len(b)
manifest={'original_sha256':hashlib.file_digest(src.open('rb'),'sha256').hexdigest(),'previous_sha256':hashlib.file_digest(Path('/usr/lib/chatgpt/resources/app.asar').open('rb'),'sha256').hexdigest(),'patched_sha256':hashlib.file_digest((out/'app.asar.bmo-fixed').open('rb'),'sha256').hexdigest(),'changed_files':list(changes),'live_verified':False}
(out/'verification.json').write_text(json.dumps(manifest,indent=2));print(manifest)
