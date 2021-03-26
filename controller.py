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
        SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
        SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
        SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                      client_secret=SPOTIFY_CLIENT_SECRET,
                                                      redirect_uri=SPOTIFY_REDIRECT_URI,
                                                      scope="user-read-currently-playing",
                                                      open_browser=False,
						                                          show_dialog=True))
        while True:
            results = sp.current_user_playing_track()

            track = results['item']
            artist = track['artists'][0]['name']
            album = track['album']['name']
            track_title = track['name']
            album_art_url = track['album']['images'][2]['url']

            def update_led(self, artist, album, track_title):
                    offscreen_canvas = self.matrix.CreateFrameCanvas()
                    font = graphics.Font()
                    font.LoadFont("../../../fonts/4x6.bdf")
                    textColor = graphics.Color(255, 255, 255)
                    pos1 = pos2 = pos3 = offscreen_canvas.width
                    pos1_tracker = pos2_tracker = pos3_tracker = -1

                    while True:
                        offscreen_canvas.Clear()
                        graphics.DrawText(offscreen_canvas, font, 12, 5, graphics.Color(255, 0, 0), 'NOW PLAYING:')

                        if (pos1_tracker == pos1 and pos2_tracker == pos2 and pos3_tracker == pos3):
                            time.sleep(5)
                            pos1 = offscreen_canvas.width
                            pos2 = offscreen_canvas.width
                            pos3 = offscreen_canvas.width
                            break
                        else:
                            pos1_tracker = pos1
                            pos2_tracker = pos2
                            pos3_tracker = pos3

                        len1 = graphics.DrawText(offscreen_canvas, font, pos1, 31, textColor, artist)
                        len2 = graphics.DrawText(offscreen_canvas, font, pos2, 23, textColor, album)
                        len3 = graphics.DrawText(offscreen_canvas, font, pos3, 15, textColor, track_title)

                        if (len1 > 64):
                            if (pos1 + len1 > 63):
                                pos1 -= 1
                        elif(pos1 > (64 - len1) / 2):
                            pos1 -= 1

                        if (len2 > 64):
                            if (pos2 + len2 > 63):
                                pos2 -= 1
                        elif(pos2 > (64 - len2) / 2):
                            pos2 -= 1

                        if (len3 > 64):
                            if (pos3 + len3 > 63):
                                pos3 -= 1
                        elif(pos3 > (64 - len3) / 2):
                            pos3 -= 1

                        time.sleep(0.07)
                        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            update_led(self, artist, album, track_title)
        
# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
