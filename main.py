import os
from criptoControl import create_app

def main():
    env = os.getenv('FLASK_ENV', 'development')
    debug = env == 'development'

    app = create_app()
    app.run(debug=debug)

if __name__ == '__main__':
    main()

