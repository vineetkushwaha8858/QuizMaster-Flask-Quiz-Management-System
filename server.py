from app import create_app

__app__ = create_app()

if __name__ == '__main__':
    __app__.run(debug=True)