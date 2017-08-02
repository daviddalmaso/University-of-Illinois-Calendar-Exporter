import mechanize
import Cookie
import cookielib
import getpass


def get_schedule_page():
  br = mechanize.Browser()
  cj = mechanize.LWPCookieJar()
  br.set_cookiejar(cj)
  br.set_handle_robots(False)   # ignore robots
  br.set_handle_equiv(True)
  br.set_handle_redirect(True)
  br.set_handle_referer(True)
  br.set_debug_responses(True)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'),('UPGRADE_INSECURE_REQUESTS', 1),('connection','keep-alive'),('accept_language', 'en-US,en;q=0.8'),('accept_encoding','gzip, deflate, br'),('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')]


  # Initial login page 
  initial_page = br.open("https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1")
  initial_page_request = br.request
  #print("Initial page response: ")
  #print(initial_page.info())
  #print("Initial page request: ")
  #print(initial_page_request.header_items())

  # Submitting login form
  br.form = list(br.forms())[0]
  br["inputEnterpriseId"] = raw_input("Enter NetID: ")
  br["password"] = getpass.getpass("Enter password: ")
  login_response = br.submit()
  login_request = br.request
  #print("Login response headers: ")
  #print(login_response.info())
  #print("Login request headers: ")
  #print(login_request.header_items())

  # Navigating to registration & records
  link_to_follow = None
  for link in br.links():
    if link.text == "Registration & Records":
      link_to_follow = link

  request = br.click_link(link_to_follow)
  response = br.follow_link(link_to_follow)
  rr_response = br.open(response.geturl())
  rr_request = br.request
  rr_info = rr_response.info()
  #print("Registration and records response: ")
  #print(rr_info)

  # Navigating to classic registration
  for link in br.links():
    if link.text == "Classic Registration":
      link_to_follow = link

  request = br.click_link(link_to_follow)
  response = br.follow_link(link_to_follow)
  cr_response = br.open(response.geturl())
  cr_request = br.request
  cr_response_info = cr_response.info()
  #print("Classic registration response: ")
  #print(cr_response_info)
  #print("Classic registration request headers: ")
  #print(cr_request.header_items())

  set_cookie_val = None
  for name, value in cr_response_info.items():
    if name == "set-cookie":
      set_cookie_val = value

  cookie_val = None
  for name, value in rr_request.header_items():
    if name == "Cookie":
      cookie_val = value

  new_cookie = set_cookie_val + "; RedirectString=https://darsweb.admin.uillinois.edu:443/darswebstu_uiuc/servlet/EASDarsServlet; " + cookie_val.split("; ", 1)[1]

  # Navigating to schedule details
  for link in br.links():
    #print(link.text)
    if link.text == 'Student Schedule - Detail':
      link_to_follow = link

  #print("Link to follow text and link to follow url")
  #print(link_to_follow.text, link_to_follow.url)

  request = br.click_link(link_to_follow)
  response = br.follow_link(link_to_follow)
  url = response.geturl()
  br.addheaders = [("Referer", "https://ui2web1.apps.uillinois.edu/BANPROD1/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu"),("Cookie", new_cookie),('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'),('UPGRADE_INSECURE_REQUESTS', 1),('connection','keep-alive'),('accept_language', 'en-US,en;q=0.8'),('accept_encoding','gzip, deflate, br'),('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')]
  #request = urllib2.Request(url, None, headers)
  sched_concise_response = br.open(url)
  #print("Response info: ")
  #print(sched_concise_response.info())

  # Submit term
  br.select_form(nr=1)
  submit_response = br.submit()
  page_contents = submit_response.read()

  file_obj = open("schedule.html", "w")
  file_obj.write(page_contents)
  file_obj.close()
