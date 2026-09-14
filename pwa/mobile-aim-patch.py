from pathlib import Path

path = Path('dist/index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    if old not in text:
        raise SystemExit(f'missing patch anchor: {label}')
    text = text.replace(old, new, 1)

text = text.replace('V3.16.3', 'V3.16.4')
text = text.replace('MOBILE CAMERA LOCK', 'RELATIVE AIM STICK')

replace_once(
    '#mobileAimZone{position:absolute;left:38%;right:0;top:0;bottom:0;',
    '#mobileAimZone{position:absolute;left:32%;right:0;top:0;bottom:0;',
    'aim-zone-width',
)
text = text.replace(
    'SOL: HAREKET · SAĞ: NİŞAN/ATEŞ · 2 PARMAK: YÖRÜNGE · KAMERA OTOMATİK',
    'SOL: HAREKET · SAĞ: SÜRÜKLE YÖN / BIRAK ATEŞ · 2 PARMAK: YÖRÜNGE',
)
text = text.replace(
    'Dokun-sürükle ile yön seç; bırakınca uyduyu fırlat.',
    'Dokunduğun noktayı merkez kabul et; istediğin yöne kısa sürükle, bırakınca ateş et.',
)

replace_once(
    'const mobileAim={pointers:new Map(),primary:null,noFire:new Set(),pinchStartDist:0,pinchStartScale:1};',
    'const mobileAim={pointers:new Map(),primary:null,noFire:new Set(),pinchStartDist:0,pinchStartScale:1,relativeActive:false};',
    'mobileAim-state',
)
replace_once(
    '''  mobileAim.primary=null;\n  mobileAim.pinchStartDist=0;\n  M.right=false;''',
    '''  mobileAim.primary=null;\n  mobileAim.pinchStartDist=0;\n  mobileAim.relativeActive=false;\n  M.right=false;''',
    'reset-relative-state',
)

anchor = '''function beginMobilePinch(){\n  if(mobileAim.pointers.size<2)return;\n  mobileAim.pinchStartDist=Math.max(20,mobilePinchDistance());\n  mobileAim.pinchStartScale=player?.scale||1;\n  for(const id of mobileAim.pointers.keys())mobileAim.noFire.add(id)\n}\n'''
helper = anchor + '''\nfunction updateRelativeMobileAim(point,clientX,clientY){\n  if(!point||!player)return false;\n\n  const dx=clientX-point.startX;\n  const dy=clientY-point.startY;\n  const d=Math.hypot(dx,dy);\n  const deadZone=14;\n\n  // A short drag behaves like a right analog stick: direction is relative\n  // to the thumb-down point, so left/right/up/down require equal travel.\n  if(d<deadZone){\n    mobileAim.relativeActive=false;\n    M.x=clientX;\n    M.y=clientY;\n    return false\n  }\n\n  const nx=dx/d;\n  const ny=dy/d;\n  const playerScreenX=(player.x-cam.x)*cam.zoom;\n  const playerScreenY=(player.y-cam.y)*cam.zoom;\n  const radius=Math.max(170,Math.min(W,H)*.42);\n\n  M.x=playerScreenX+nx*radius;\n  M.y=playerScreenY+ny*radius;\n  mobileAim.relativeActive=true;\n  return true\n}\n'''
replace_once(anchor, helper, 'relative-aim-helper')

replace_once(
    '''    mobileAim.pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});\n    if(mobileAim.primary==null)mobileAim.primary=e.pointerId;\n    M.x=e.clientX;M.y=e.clientY;\n    if(mobileAim.pointers.size===2)beginMobilePinch()''',
    '''    mobileAim.pointers.set(e.pointerId,{\n      x:e.clientX,y:e.clientY,\n      startX:e.clientX,startY:e.clientY\n    });\n    if(mobileAim.primary==null)mobileAim.primary=e.pointerId;\n    if(mobileAim.primary===e.pointerId){\n      mobileAim.relativeActive=false;\n      M.x=e.clientX;M.y=e.clientY\n    }\n    if(mobileAim.pointers.size===2)beginMobilePinch()''',
    'aim-pointerdown',
)
replace_once(
    '''    mobileAim.pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});\n    if(mobileAim.pointers.size>=2){''',
    '''    const point=mobileAim.pointers.get(e.pointerId);\n    point.x=e.clientX;point.y=e.clientY;\n    if(mobileAim.pointers.size>=2){''',
    'aim-pointermove-state',
)
replace_once(
    '''    }else if(mobileAim.primary===e.pointerId){\n      M.x=e.clientX;M.y=e.clientY\n    }\n  });''',
    '''    }else if(mobileAim.primary===e.pointerId){\n      updateRelativeMobileAim(point,e.clientX,e.clientY)\n    }\n  });''',
    'aim-pointermove-direction',
)
replace_once(
    '''  function endAim(e){\n    if(!mobileAim.pointers.has(e.pointerId))return;\n    e.preventDefault();\n    M.x=e.clientX;M.y=e.clientY;\n    const wasPrimary=mobileAim.primary===e.pointerId;\n    const blocked=mobileAim.noFire.has(e.pointerId);''',
    '''  function endAim(e){\n    if(!mobileAim.pointers.has(e.pointerId))return;\n    e.preventDefault();\n    const point=mobileAim.pointers.get(e.pointerId);\n    const wasPrimary=mobileAim.primary===e.pointerId;\n    if(wasPrimary&&mobileAim.pointers.size===1){\n      updateRelativeMobileAim(point,e.clientX,e.clientY)\n    }\n    const blocked=mobileAim.noFire.has(e.pointerId);''',
    'aim-pointerup-direction',
)
replace_once(
    '''    if(!mobileAim.pointers.size){\n      mobileAim.noFire.clear();\n      mobileAim.primary=null\n    }\n''',
    '''    if(!mobileAim.pointers.size){\n      mobileAim.noFire.clear();\n      mobileAim.primary=null;\n      mobileAim.relativeActive=false\n    }\n''',
    'aim-release-reset',
)

path.write_text(text, encoding='utf-8')
