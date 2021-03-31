import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        def update_led(self, artist, album, track_title, offscreen_canvas, font):
            textColor = graphics.Color(255, 255, 255)
            global previous_track
            global pos1_tracker
            global pos2_tracker
            global pos3_tracker
            global pos1
            global pos2
            global pos3
            if track != previous_track:
                previous_track = track
                pos1 = offscreen_canvas.width
                pos2 = offscreen_canvas.width
                pos3 = offscreen_canvas.width
                pos1_tracker = -1
                pos2_tracker = -1
                pos3_tracker = -1

            while True:
                offscreen_canvas.Clear()
                graphics.DrawText(offscreen_canvas, font, 9, 5, graphics.Color(255, 0, 0), 'NOW PLAYING:')


                len1 = graphics.DrawText(offscreen_canvas, font, pos1, 31, textColor, artist)
                len2 = graphics.DrawText(offscreen_canvas, font, pos2, 23, textColor, album)
                len3 = graphics.DrawText(offscreen_canvas, font, pos3, 15, textColor, track_title)

                if (pos1_tracker == pos1 and pos2_tracker == pos2 and pos3_tracker == pos3):
                    time.sleep(3)
                    if len1 > 65:
                        pos1 = offscreen_canvas.width
                    if len2 > 65:
                        pos2 = offscreen_canvas.width
                    if len3 > 65:
                        pos3 = offscreen_canvas.width
                    break
                else:
                    pos1_tracker = pos1
                    pos2_tracker = pos2
                    pos3_tracker = pos3

                if (len1 > 65):
                    if (pos1 + len1 > 65):
                        pos1 -= 1
                elif(pos1 > (65 - len1) / 2):
                    pos1 -= 1

                if (len2 > 65):
                    if (pos2 + len2 > 65):
                        pos2 -= 1
                elif(pos2 > (65 - len2) / 2):
                    pos2 -= 1

                if (len3 > 65):
                    if (pos3 + len3 > 65):
                        pos3 -= 1
                elif(pos3 > (65 - len3) / 2):
                    pos3 -= 1

                time.sleep(0.07)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
        SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
        SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                      client_secret=SPOTIFY_CLIENT_SECRET,
                                                      redirect_uri=SPOTIFY_REDIRECT_URI,
                                                      scope="user-read-currently-playing",
                                                      open_browser=False,
						                              show_dialog=True))
        previous_track = None
        pos1 = pos2 = pos3 = 0
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/4x6.bdf")
        while True:
            try:
                results = sp.current_user_playing_track()
            except Exception as e:
                print(e)
                continue
            if results is not None:
                track = results['item']
                if len(track['artists']) >= 0:
                    artist = track['artists'][0]['name']
                else:
                    artist = ' '
                album = track['album']['name']
                track_title = track['name']
                album_art_url = track['album']['images'][2]['url']
                update_led(self, artist, album, track_title, offscreen_canvas, font)
            else:
                offscreen_canvas.Clear()
                #graphics.DrawText(offscreen_canvas, font, 12, 5, graphics.Color(255, 0, 0), 'PAUSED')
                time.sleep(1)
        
# Main function
if __name__ == "__main__":
    run_text = RunText()
    previous_track = None
    pos1_tracker = -1
    pos2_tracker = -1
    pos3_tracker = -1
    if (not run_text.process()):
        run_text.print_help()