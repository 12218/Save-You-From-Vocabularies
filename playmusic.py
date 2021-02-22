import mp3play
import time

clip = mp3play.load('./mp3/audio.mp3')
clip.play()
time.sleep(5)
clip.stop()