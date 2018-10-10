from player_gtkapplication import PlayerGtkApplication
import sys

if __name__ == '__main__':
    app = PlayerGtkApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)