from flask import *

from src.database import *
import datetime
from src.newcnn import predictcnn

import json
from web3 import Web3, HTTPProvider

# truffle development blockchain address
blockchain_address = 'HTTP://127.0.0.1:7545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = r'C:\Users\HP\Downloads\scrap_net (5)\scrap_net\src\node_modules\.bin\build\contracts\vehicleinfo.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0xD887D746B1a69f35B8c85CAf98a506AaCE40692c'


app=Flask(__name__)

app.secret_key="aaaaaaaaaaa"


# import functools
# def login_required(func):
#     @functools.wraps(func)
#     def secure_function():
#         if "lid" not in session:
#             return redirect ("/")
#         return func()
#     return secure_function

@app.route("/logout")
# #@login_required

def logout():
    session.clear()
    return render_template("login_index.html")

@app.route('/')
def start():
    return render_template('login_index.html')

@app.route('/logincode',methods=['post'])
def logincode():
    uname=request.form['textfield']
    pwd=request.form['textfield2']
    qry="select * from login where username=%s and password=%s"
    val=(uname,pwd)
    print(val)
    res=selectone(qry,val)
    print(res)
    if res is None:
        return '''<script>alert(" Invalid Username or Password ");window.location="/"</script>'''
    elif res[3]=="admin":
        session['lid']=res[0]

        return '''<script>alert("Admin login success ");window.location="/rtohome"</script>'''
    elif res[3] == "scraper":
        session['lid'] = res[0]
        return '''<script>alert(" login success ");window.location="/scraphome"</script>'''
    elif res[3] == "user":
        session['lid'] = res[0]
        return '''<script>alert("User login success ");window.location="/userhome"</script>'''

    else:
        return '''<script>alert("Invalid Username or Password");window.location="/"</script>'''



@app.route('/acceptrejectscrap')
#@login_required
def acceptrejectscrap():
    qry="SELECT `scrap`.*,`login`.`type` FROM `scrap` JOIN `login` ON `scrap`.`lid`=`login`.`id` WHERE `login`.`type`='pending'"
    res=selectall(qry)
    return render_template('rto/accept reject scrap.html',val=res)

@app.route('/acceptscrap')
#@login_required
def acceptscrap():
    id = request.args.get('id')
    qry = "update login set type='scraper' where id=%s"
    val = id
    print(val)
    iud(qry, val)
    return '''<script>alert("Accepted..");window.location="/acceptrejectscrap"</script>'''

@app.route('/rejectscrap')
#@login_required
def rejectscrap():
    id = request.args.get('id')
    qry = "update login set type='reject' where id=%s"
    val = id
    print(val)
    iud(qry, val)
    return '''<script>alert("Rejected..");window.location="/acceptrejectscrap"</script>'''

@app.route('/acceptedscrap')
#@login_required
def acceptedscrap():
    qry="SELECT `scrap`.*,`login`.`type` FROM `scrap` JOIN `login` ON `scrap`.`lid`=`login`.`id` WHERE `login`.`type`='scraper'"
    res=selectall(qry)
    return render_template('rto/accepted scrap.html',val=res)

@app.route('/rtohome')
#@login_required
def rtohome():
    return render_template('rto/rto_index.html')

@app.route('/sendreply')
#@login_required
def sendreply():
    id=request.args.get('id')
    session['rid']=str(id)
    return render_template('rto/send reply.html')


@app.route('/reply',methods=['post'])
#@login_required
def reply():

    reply=request.form['textarea']
    qry = "update `complaint` SET `reply`=%s WHERE `id`=%s"
    val =(reply,session['rid'])
    print(val)
    iud(qry, val)
    return '''<script>alert("Replyed..");window.location="/viewcomplaintreply"</script>'''

@app.route('/viewscraprating')
#@login_required
def viewscraprating():
    qry="SELECT `scrap`.`fname`,`scrap`.`lname`,`user`.`fname`,`user`.`lname`,`rating`.* FROM `scrap` JOIN `rating` ON `rating`.`slid`=`scrap`.`lid` JOIN `user` ON `user`.`lid`=`rating`.`ulid`"
    res=selectall(qry)
    return render_template('rto/view scraprating.html',val=res)

@app.route('/viewcomplaintreply')
#@login_required
def viewcomplaintreply():
    qry="SELECT `user`.`fname`,`lname`,`complaint`.* FROM `complaint` JOIN `user` ON `user`.`lid`=`complaint`.`lid` where `complaint`.reply='pending' "
    res=selectall(qry)
    return render_template('rto/viewcomplaint reply bn.html',val=res)


@app.route('/viewcar')
#@login_required
def viewcar():
    qry="SELECT `user`.`fname`,`lname`,`car_details`.*,`scraprequest`.`status`,`scraprequest`.`id`  FROM `user` JOIN`car_details` ON `car_details`.`lid`=`user`.`lid` JOIN `scraprequest` ON `scraprequest`.`carid`=`car_details`.`id` where `scraprequest`.`status`='price ok' and `car_details`.`id` NOT IN (SELECT `cid` FROM `carstatus`)"
    res=selectall(qry)
    print(res)
    return render_template('rto/viewcar.html',val=res)

@app.route('/vcar')
# @login_required
def vcar():
    id=request.args.get('id')
    qry="SELECT * FROM `car_details` WHERE `id`=%s"
    res=selectone(qry,id)
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        d = datetime.datetime.now().strftime("%Y-%m-%d")
        vifo=str(res[2]+","+res[3]+","+res[4]+","+res[5])
        #  function add_info(uint _bid,uint _uid,uint _vehid,string memory _vehinfo,string memory _date)public{
        message2 = contract.functions.add_info(blocknumber + 1, int(res[1]), int(res[0]),  vifo, d).transact()
        print (message2,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    qry = "INSERT INTO `carstatus` VALUES(%s)"
    iud(qry, id)
    qq="UPDATE `scraprequest` SET`status`='Accepted by RTO' WHERE `carid`=%s"
    iud(qq,id)
    return redirect("/viewcar")

# __________________________scrap______________________________________

@app.route('/addpriceinfo')
#@login_required
def addpriceinfo():
    id = session['lid']
    qry="SELECT `car_details`.*,`scraprequest`.`id`,`scraprequest`.`status` FROM `car_details` JOIN `scraprequest` ON `car_details`.`id`=`scraprequest`.`carid` WHERE `scraprequest`.`lid`=%s and scraprequest.status !='pending'"
    res=selectall2(qry,id)
    print(res)
    return render_template('scrap/add price info.html',val=res)


@app.route('/certificateup')
#@login_required
def certificateup(): 
    id = request.args.get('id')
    session['cid'] = id
    return render_template('scrap/cinfo.html')


@app.route('/priceinfo')
#@login_required
def priceinfo():
    id = request.args.get('id')
    session['pid']=id
    return render_template('scrap/price info.html')

@app.route('/priceinfocode',methods=['post'])
#@login_required
def priceinfocode():
    id=session['pid']
    price=request.form['textfield']
    qry="insert into `price_info` VALUES(NULL,%s,%s)"
    val=(id,price)
    print(val)
    iud(qry,val)
    return'''<script>alert("added..");window.location="/addpriceinfo"</script>'''

@app.route('/cerinfocode',methods=['post'])
#@login_required
def cerinfocode():
    id=session['cid']
    img=request.files['img']
    fn=str(id)+".png"
    img.save("static/certificate/"+fn)
    qry="INSERT INTO `certificate` VALUES(NULL,%s,%s,%s,CURDATE())"
    val=(id,session['lid'],fn)
    print(val)
    iud(qry,val)
    q="UPDATE `scraprequest` SET `status`='Certified' WHERE `carid`=%s"
    iud(q,id)
    return'''<script>alert("added..");window.location="/addpriceinfo"</script>'''

@app.route('/scraphome')
def scraphome():
    return render_template('scrap/scrap_index.html')

@app.route('/scrapregistration')
#@login_required
def scrapregistration():
    return render_template('reg_index.html')



@app.route('/register1',methods=['post'])

def register1():
    fname=request.form['textfield']
    lname = request.form['textfield9']
    place=request.form['textfield2']
    post=request.form['textfield3']
    pin=request.form['textfield4']
    phone=request.form['textfield5']
    email=request.form['textfield6']
    username=request.form['textfield7']
    password=request.form['textfield8']
    # lati=request.form['lati']
    # longi=request.form['longi']
    qry="insert into login values(null,%s,%s,'pending')"
    val=(username,password)
    id=iud(qry,val)
    qry="insert into scrap values(null,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(id,fname,lname,place,post,pin,email,phone)
    iud(qry,val)

    # qr="INSERT INTO `location` VALUES (NULL,%s,%s,%s)"
    # v=(id,lati,longi)
    # iud(qr,v)

    return '''<script>alert("You can Login after the Admin Confirmation...");window.location="/"</script>'''

@app.route('/viewrating')
#@login_required
def viewrating():
    id = session['lid']
    qry="SELECT `user`.`fname`,`lname`,`rating`.* FROM `rating` JOIN `user` ON `user`.`lid`=`rating`.`ulid` WHERE `rating`.`slid`=%s"
    res=selectall2(qry,id)
    return render_template('scrap/view rating.html',val=res)

@app.route('/viewrequestandverifycardetails')
#@login_required
def viewrequestandverifycardetails():
    id=session['lid']
    qry="SELECT `user`.`fname`,`lname`,`car_details`.* ,`scraprequest`.`date`,`scraprequest`.`id`,`scraprequest`.`status` FROM `user` JOIN`car_details` ON `car_details`.`lid`=`user`.`lid` JOIN `scraprequest` ON `scraprequest`.`carid`=`car_details`.`id` WHERE `scraprequest`.`lid`=%s"
    res=selectall2(qry,id)
    print(res)
    return render_template('scrap/view request andverify cardetails.html',val=res)

@app.route('/verify')
#@login_required
def verify():
    id = request.args.get('id')
    qry = "update `scraprequest` SET `status`='verified by Scraper' WHERE `id`=%s"
    val = id
    print(val)
    iud(qry, val)
    return '''<script>alert("Verifyed..");window.location="/viewrequestandverifycardetails"</script>'''
# _____________________________________user__________________________________________________


@app.route('/userhome')
def userhome():
    return render_template('user/user_index.html')

@app.route('/priceinfo_user')
#@login_required
def priceinfo_user():
    qry="SELECT `price_info`.`reqid`,`price`,`scrap`.`fname`,`scrap`.`lname`,`car_details`.`car_model`,`scraprequest`.`date` FROM `price_info` JOIN `scraprequest` ON `scraprequest`.`id`=`price_info`.`reqid` JOIN `scrap` ON `scrap`.`lid`=`scraprequest`.`lid` JOIN `car_details` ON `car_details`.`id`=`scraprequest`.`carid` WHERE `car_details`.`lid`=%s"
    val=(session['lid'])
    res=selectall2(qry,val)

    return render_template('user/price.html',val=res)

@app.route('/priceinfo_user1')
#@login_required
def priceinfo_user1():
    id=request.args.get("id")
    from src.newcnn import predictcnn

    # res=predictcnn("static/carimg/"+str(id)+".png")
    res=predictcnn(r"C:\Users\HP\Downloads\scrap_net\src\static\carimg\5.png")
    msg="50 "
    if str(res)=="0":
        msg="10"
    elif str(res)=="1":
        msg="30"
    print (msg)
    return "<script>alert("+str(msg)+");window.location='/priceinfo_user'</script>"

@app.route('/acceptbyuser')
#@login_required
def acceptbyuser():
    id=request.args.get("id")
    qry="UPDATE `scraprequest` SET `status`='accepted' WHERE `id`=%s"
    iud(qry,id)

    return redirect("/requeststatus")


@app.route('/cardetails')
#@login_required
def cardetails():

    return render_template('user/car details.html')
@app.route('/carcode',methods=['post'])
#@login_required
def carcode():
    model = request.form["textfield"]
    engine = request.form["textfield2"]
    chases = request.form["textfield3"]
    seater = request.form["textfield4"]
    regno = request.form["textfield5"]
    fltyp = request.form["textfield52"]
    condition = request.form["radiobutton"]
    regyear = request.form["textfield522"]
    wheel = request.form["textfield523"]
    qry = "INSERT INTO `car_details` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (session['lid'], model, engine, chases, seater,regno,fltyp,condition,regyear,wheel)
    iud(qry, val)
    return '''<script>alert(" Successfully Added...");window.location="/userhome"</script>'''


@app.route('/requestforscrap')
#@login_required
def requestforscrap():
    qry="select scrap.*,login.* from scrap join login on scrap.lid=login.id where login.type='scraper'"
    res=selectall(qry)
    print(res)
    return render_template('user/request for scrap.html',val=res)


@app.route('/requeststatus')
#@login_required
def requeststatus():
    id=session['lid']
    qry="SELECT `scrap`.`fname`,`lname`,`scraprequest`.`status`,`date`,`car_details`.`lid`,`scraprequest`.`id`,`price_info`.`price` FROM `car_details`  JOIN `scraprequest` ON `scraprequest`.`carid`=`car_details`.`id` JOIN `scrap` ON `scrap`.`lid`=`scraprequest`.`lid` LEFT JOIN `price_info` ON `price_info`.`reqid`=`scraprequest`.`id` WHERE `car_details`.`lid`=%s"
    res=selectall2(qry,id)
    print(res)
    return render_template('user/request status.html',val=res)

0

@app.route('/viewreplyandsendcomplaint',methods=['post','get'])
#@login_required
def viewreplyandsendcomplaint():
    qry="SELECT * FROM `complaint` where lid=%s"
    val=(session['lid'])
    res=selectall2(qry,val)
    return render_template('user/view reply and send complaint.html',val=res)

@app.route('/acceptprice')
#@login_required
def acceptprice():
    id = request.args.get('id')
    qry = "update scraprequest set status='price ok' where id=%s"
    val = id
    print(val)
    iud(qry, val)
    return '''<script>alert("Price Accepted..");window.location="/requeststatus"</script>'''

@app.route('/rejectprice')
#@login_required
def rejectprice():
    id = request.args.get('id')
    qry = "update scraprequest set status='Price rejected' where id=%s"
    val = id
    print(val)
    iud(qry, val)
    return '''<script>alert("Price Rejected..");window.location="/requeststatus"</script>'''


@app.route('/sendcomplaint',methods=['post'])
#@login_required
def sendcomplaint():
    return render_template('user/send complaint.html')

@app.route('/sendcomplaintcode',methods=['post'])
#@login_required
def sendcomplaintcode():
    complaint=request.form['textarea']
    qry="insert into complaint values(null,%s,%s,'pending',curdate())"
    val=(session['lid'],complaint)
    iud(qry,val)


    return '''<script>alert("successfully Added...");window.location="/viewreplyandsendcomplaint"</script>'''



# @app.route('/sendrating',methods=['post','get'])
# #@login_required
# def sendrating():
#     qry="select * from scrap"
#     res=selectall(qry)
#     return render_template('user/send rating.html',val=res)
# @app.route('/sendratingcode',methods=['post'])
# #@login_required
# def sendratingcode():
#     scrapid = request.form['select']
#     rating=request.form['textfield']
#     qry="INSERT INTO `rating` VALUES (NULL,%s,%s,%s,CURDATE())"
#     val=(session['lid'],scrapid,rating)
#     print(val)
#     iud(qry,val)


#     return '''<script>alert("successfully Added...");window.location="/viewscrapratinguser"</script>'''


# @app.route('/sendrequest')
# #@login_required
# def sendrequest():
#     id=request.args.get('id')
#     qry="select * from scrap where lid=%s"
#     res=selectall2(qry,str(id))
#     qry1="select * from car_details where lid=%s"
#     val1=session['lid']
#     res1=selectall2(qry1,val1)
#     return render_template('user/send request.html',val=res,val1=res1)

# @app.route('/sendrequestcode',methods=['post'])
# #@login_required
# def sendrequestcode():
#     lid=request.form['select']
#     carid=request.form['select2']
#     img=request.files['img']
#     qry="insert into scraprequest values(null,%s,%s,'pending',curdate())"
#     val=(lid,carid)
#     id=iud(qry,val)
#     img.save("static/carimg/"+str(id)+".png")

#     return '''<script>alert("successfully added...");window.location="/requestforscrap"</script>'''


# @app.route('/userregistration')
# def userregistration():
#     return render_template('user/usr_reg_index.html')

# @app.route('/register2',methods=['post'])
# def register2():
#     fname=request.form['textfield']
#     lname = request.form['textfield1']
#     gender = request.form['radiobutton']
#     place=request.form['textfield2']
#     post=request.form['textfield3']
#     pin=request.form['textfield4']
#     phone=request.form['textfield5']
#     email=request.form['textfield6']
#     username=request.form['textfield7']
#     password=request.form['textfield8']
#     qry="insert into login values(null,%s,%s,'user')"
#     val=(username,password)
#     id=iud(qry,val)
#     qry="insert into user values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#     val=(id,fname,lname,gender,place,post,pin,email,phone)
#     iud(qry,val)
#     return '''<script>alert("Success");window.location="/"</script>'''

# @app.route('/viewscrapratinguser',methods=['post','get'])
# #@login_required
# def viewscrapratinguser():
#     qry="SELECT `user`.`fname`,`lname`,`rating`.* FROM `rating` JOIN `user` ON `rating`.`ulid`=`user`.`lid` WHERE `rating`.`ulid`=%s"
#     val=session['lid']
#     res=selectall2(qry,val)
#     return render_template('user/view scrap rating.html',val=res)

# @app.route('/viewscrapedcertificate')
# #@login_required
# def viewscrapedcertificate():
#     id=session['lid']
#     print(id)
#     qry="SELECT `car_details`.`car_model`,`regno`,`certificate`.*,`scraprequest`.`lid` FROM `car_details` JOIN `scraprequest` ON `scraprequest`.`carid`=`car_details`.`id` JOIN `certificate` ON `certificate`.`reqid`=`scraprequest`.`id` where `car_details`.`lid`=%s"
#     res=selectall2(qry,id)
#     return render_template('user/view scraped certificate.html',val=res)




app.run(debug=True,port=5001)