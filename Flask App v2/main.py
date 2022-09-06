from website import create_app

application = create_app()

if __name__ == '__main__': # only if we run this file, we execute line 6. 
  application.run(debug=True) # it runs the server if we run main.py