from django.shortcuts import render, redirect
from .models import Beneficiary, Sender, Receipt
from django.contrib.auth.models import auth, User
from django.contrib import messages
import datetime





def index(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        psw = request.POST['psw']

        user = auth.authenticate(username=uname, password=psw)
        if user is not None:
            auth.login(request, user)
            return redirect('/ben')
        else:
            messages.info(request, 'Username Or Password Is Wrong!')
            return redirect('/')


    else:
        return render(request, 'index.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
#---BENEFICIARY---
def beneficiary(request):
    if request.method == 'POST':
        # Check for data to be posted
        btn = request.POST['btn']
        # check button status
        if btn == 'Search':
            receiverCheck = request.POST['search']
            # searching throw database
            if Beneficiary.objects.filter(byOrder = receiverCheck).exists():
                ben = Beneficiary.objects.get(byOrder = receiverCheck)
                allBen = Beneficiary.objects.all()
                return render(request, 'beneficiary.html', {'benInfo': ben, 'allB': allBen})
            else:
                messages.info(request, 'Nothing found!')
                allBen = Beneficiary.objects.all()
                return render(request, 'beneficiary.html', {'allB': allBen})
        else:
            receiver = request.POST['receiver']
            if Beneficiary.objects.filter(byOrder = receiver).exists():
                ben = Beneficiary.objects.get(byOrder = receiver)
                return redirect(f'/{receiver}/')
            else:
                receiverNo = request.POST['receiverNo']
                selectCountry = request.POST['country']
                if selectCountry == 'Not-In-The-List':
                    country = request.POST['country-2']
                    city = request.POST['city-2']
                else:
                    country = selectCountry
                    city = request.POST['city']
                nationality = request.POST['nationality']

                newBeneficiary = Beneficiary.objects.create(
                    byOrder = receiver,
                    receiverNo  = receiverNo,
                    country = country,
                    city = city,
                    nationality = nationality
                )
                newBeneficiary.save();
                ben = Beneficiary.objects.get(byOrder = receiver)
                return redirect(f'/{receiver}/')
    else:
        allBen = Beneficiary.objects.all()
        return render(request, 'beneficiary.html', { 'allB': allBen}) 

#---SENDER---
def sender(request, ben):
    if request.method == 'POST':
        ben = Beneficiary.objects.get(byOrder = ben)
        # Check for data to be posted
        btn = request.POST['btn']
        # check button status
        if btn == 'Search':
            senderCheck = request.POST['search']
            if Sender.objects.filter(sender = senderCheck).exists():
                senderInfo = Sender.objects.get(sender = senderCheck)
                allSenders = Sender.objects.all()
                return render(request, 'sender.html', {'senInf': senderInfo, 'allSs': allSenders})
            else:
                messages.info(request, 'Nothing found!')
                allSenders = Sender.objects.all()
                return render(request, 'sender.html', {'allSs': allSenders})
        else:
            sender = request.POST['sender']
            address = request.POST['address']
            tel2 = request.POST['tel2']
            idNo = request.POST['id-no']
            porpuse = request.POST['porpuse']
            if Sender.objects.filter(sender = sender).exists():
                return redirect(f'/{ben.byOrder}/{sender}/')
            else:

                newSender = Sender.objects.create(
                    sender = sender,
                    address = address,
                    senderNo = tel2,
                    idNo = idNo,
                    porpuse = porpuse
                )
                newSender.save();
                #ben = Beneficiary.objects.get(byOrder = ben)
                return redirect(f'/{ben.byOrder}/{sender}/')
    else:
        ben = Beneficiary.objects.get(byOrder = ben)
        allSenders = Sender.objects.all()
        return render(request, 'sender.html', {'ben': ben, 'allSs': allSenders})
        

#---Receipt---    
def receipt(request, ben, sender):
    time = datetime.datetime.now()
    if request.method == 'POST':
        sender = Sender.objects.get(sender = sender)
        ben = Beneficiary.objects.get(byOrder = ben)
        payOut = request.POST['pay-out']
        rate = request.POST['rate']
        charge = request.POST['charge']
        psw = request.POST['psw']
        nowTime = time.strftime("%X")
        nowDate = time.strftime("%x")
        if Receipt.objects.filter(receiver = ben.byOrder,sender = sender.sender,payoutAmtUsd = payOut,rate = rate,charge = charge,password = psw, time = nowTime,valueDate = nowDate).exists():
            receiptId = Receipt.objects.get(receiver = ben.byOrder,sender = sender.sender,payoutAmtUsd = payOut,rate = rate,charge = charge,password = psw, time = nowTime,valueDate = nowDate)
            return redirect(f'/{ben.byOrder}/{sender.sender}/{receiptId.id}')
        
        else:
            newReceipt = Receipt.objects.create(
                receiver = ben.byOrder,
                sender = sender.sender,
                payoutAmtUsd = payOut,
                rate = rate,
                charge = charge,
                password = psw,
                time = nowTime,
                valueDate = nowDate
            )
            newReceipt.save();
            receiptId = Receipt.objects.get(receiver = ben.byOrder,sender = sender.sender,payoutAmtUsd = payOut,rate = rate,charge = charge,password = psw, time = nowTime,valueDate = nowDate)
            return redirect(f'/{ben.byOrder}/{sender.sender}/{receiptId.id}')
    else:
        ben = Beneficiary.objects.get(byOrder = ben)
        sender = Sender.objects.get(sender = sender)
        return render(request, 'receipt.html', {'ben': ben, 'sender': sender})


#---PDF---
def pdf(request, ben, sender, receipt):
    benInfo = Beneficiary.objects.get(byOrder = ben)
    senderInfo = Sender.objects.get(sender = sender)
    receiptInfo = Receipt.objects.get(id = receipt)
    pay_amt = float(receiptInfo.payoutAmtUsd) 
    charge_amt = float(receiptInfo.charge)
    rate_amt = float(receiptInfo.rate)
    sending_amt = float(receiptInfo.rate) * float(receiptInfo.payoutAmtUsd)
    total_amt = sending_amt + float(receiptInfo.charge)
    return render(request, 'pdf.html', {'ben': ben, 'sender': sender, 'receipt': receipt, 'bInf': benInfo, 'sInf': senderInfo, 'rInf': receiptInfo, 'rateAmt': f'{rate_amt:,.7f}','payAmt': f'{pay_amt:,.2f}', 'chargeAmt': f'{charge_amt:,.2f}','sendingAmt': f'{sending_amt:,.2f}', 'totalAmt': f'{total_amt:,.2f}'})
