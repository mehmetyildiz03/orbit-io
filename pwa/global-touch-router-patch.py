from pathlib import Path

path = Path('dist/index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    if old not in text:
        raise SystemExit(f'missing patch anchor: {label}')
    text = text.replace(old, new, 1)

text = text.replace('V3.16.5', 'V3.16.6')
text = text.replace('FULL-SCREEN AIM', 'GLOBAL TOUCH ROUTER')
text = text.replace(
    'JOYSTICK: HAREKET · DİĞER HER YER: NİŞAN / BIRAK ATEŞ · 2 PARMAK: YÖRÜNGE',
    'JOYSTICK: HAREKET · DİĞER HER PİKSEL: NİŞAN / BIRAK ATEŞ · 2 PARMAK: YÖRÜNGE',
)
text = text.replace(
    'Joystick ve Black Hole düğmesi dışında ekranın herhangi bir yerine dokun; sürükle yön seçer, bırakınca ateş eder.',
    'Joystick ve Black Hole düğmesi dışında ekranın herhangi bir pikseline dokun; sürükle yön seçer, bırakınca ateş eder.',
)

replace_once(
    'body.touch-mode #mobileControls.active{display:block;position:fixed;inset:0;z-index:7;pointer-events:none}',
    'body.touch-mode #mobileControls.active{display:block;position:fixed;inset:0;z-index:7;pointer-events:auto;touch-action:none}',
    'controls-own-touch-surface',
)
replace_once(
    '#mobileAimZone{position:absolute;left:0;right:0;top:0;bottom:0;z-index:0;pointer-events:auto;touch-action:none;background:transparent}',
    '#mobileAimZone{position:absolute;left:0;right:0;top:0;bottom:0;z-index:0;pointer-events:none;touch-action:none;background:transparent}',
    'aim-zone-noninteractive',
)
replace_once(
    "const joy=$('joyPad'),stick=$('joyStick'),aimZone=$('mobileAimZone'),bh=$('bhTouch');\n  if(!joy||!stick||!aimZone||!bh)return;",
    "const controls=$('mobileControls'),joy=$('joyPad'),stick=$('joyStick'),aimZone=$('mobileAimZone'),bh=$('bhTouch');\n  if(!controls||!joy||!stick||!aimZone||!bh)return;",
    'controls-root-ref',
)
replace_once(
    "aimZone.addEventListener('pointerdown',e=>{\n    if(e.pointerType==='mouse'||!running)return;\n    e.preventDefault();",
    "controls.addEventListener('pointerdown',e=>{\n    if(e.pointerType==='mouse'||!running)return;\n    if(e.target.closest&&e.target.closest('#joyPad,#bhTouch'))return;\n    e.preventDefault();",
    'root-pointerdown',
)
replace_once(
    'if(aimZone.setPointerCapture)aimZone.setPointerCapture(e.pointerId);',
    'if(controls.setPointerCapture)controls.setPointerCapture(e.pointerId);',
    'root-pointer-capture',
)
replace_once(
    "aimZone.addEventListener('pointermove',e=>{",
    "controls.addEventListener('pointermove',e=>{",
    'root-pointermove',
)
replace_once(
    "aimZone.addEventListener('pointerup',endAim);",
    "controls.addEventListener('pointerup',endAim);",
    'root-pointerup',
)
replace_once(
    "aimZone.addEventListener('pointercancel',endAim);",
    "controls.addEventListener('pointercancel',endAim);",
    'root-pointercancel',
)
replace_once(
    "navigator.serviceWorker.register('./service-worker.js').catch(()=>{})",
    "navigator.serviceWorker.register('./service-worker.js',{updateViaCache:'none'}).then(reg=>reg.update()).catch(()=>{})",
    'force-sw-update',
)
replace_once(
    'const mobileInput={moveX:0,moveY:0,moveActive:false,joyPointer:null,bhPointer:null};',
    "const MOBILE_BUILD='3.16.6-global-router';\nconst mobileInput={moveX:0,moveY:0,moveActive:false,joyPointer:null,bhPointer:null};",
    'build-marker',
)

checks = [
    'V3.16.6',
    'GLOBAL TOUCH ROUTER',
    "MOBILE_BUILD='3.16.6-global-router'",
    "controls.addEventListener('pointerdown'",
    "controls.addEventListener('pointermove'",
    "controls.addEventListener('pointerup',endAim)",
    "e.target.closest('#joyPad,#bhTouch')",
    'pointer-events:auto;touch-action:none',
    '#mobileAimZone{position:absolute;left:0;right:0;top:0;bottom:0;z-index:0;pointer-events:none',
    "updateViaCache:'none'",
]
for token in checks:
    if token not in text:
        raise SystemExit('missing ' + token)
if "aimZone.addEventListener('pointerdown'" in text:
    raise SystemExit('old aimZone pointer router remains')

path.write_text(text, encoding='utf-8')
