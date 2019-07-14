let mFlag, sTime, eTime, sClientX, eClientX
let time = []
let track = []

btn = document.querySelector('.nc_iconfont.btn_slide')

function mouseDown(e) {
  sTime = new Date().getTime()
  mFlag = true
  sClientX = e.clientX

  time.push(0)
  track.push(0)
}

function mouseUp(e) {
  eTime = new Date().getTime()
  mFlag = false
  eClientX = e.clientX
  time.push(eTime - sTime)
  track.push(eClientX - sClientX)

  console.log(time.toString())
  console.log(track.toString())

  var blob = new Blob([time.toString() + '\n\n' + track.toString()], { type: 'text/plain' })
  a = document.createElement('a')
  a.download = 'recorder.txt'
  a.href = window.URL.createObjectURL(blob)
  a.dataset.downloadurl = ['text/plain', a.download, a.href].join(':')

  me = document.createEvent('MouseEvents')
  me.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
  a.dispatchEvent(me)

  time = []
  track = []
}


function mouseMove(e) {
  if (mFlag) {
    time.push(new Date().getTime() - sTime)
    track.push(e.clientX - sClientX)
  }
}

btn.addEventListener('mousedown', mouseDown, null)
btn.addEventListener('mouseup', mouseUp, null)
btn.addEventListener('mousemove', mouseMove)

