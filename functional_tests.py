from selenium import webdriver
broswer = webdriver.Firefox()
broswer.get('http://localhost:8000')
assert 'Django' in broswer.title
