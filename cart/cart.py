from store.models import Product
from decimal import Decimal


class Cart():
    def __init__(self,request):
        self.session=request.session
        #btrj3 lsession lal user
        cart=self.session.get('session_key')
        #eza howe newuser bt3mlo create la session
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
        # la y3rf eza luser 3ind cart aw la
        self.cart=cart


    def add(self,product,product_qty):
        product_id=str(product.id)
        if product_id  in self.cart:
            self.cart[product_id]['qty']=product_qty #eza lproduct b2lb lcard bas badna n7ot lqunatity

        else:
            self.cart[product_id]={'price':str(product.price), 'qty':product_qty} # eza mish mawjod lproduct bel cart badna nzid lprice w qunatity

        self.session.modified=True # mn3ml update lal session


    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        all_product_ids=self.cart.keys()#mnjeeb lproduct ids lb2lb lcart hene lkeys lal cart
        products=Product.objects.filter(id__in=all_product_ids)#mnjeeb min ldatabase kel lproduct ids 3a shart ykono equal lale bel cart
        cart=self.cart.copy()#mnjeeb copy lal cart

        for product in products:
            cart[str(product.id)]['product']=product #3atyna lal copy cart product id ljbna min database 3asehen yser fena nst5dm shi 8er lid w qunatity
        for item in cart.values():
            item['price']=Decimal(item['price']) #brl add fo2 ana m3rf price w qty lezm ykono nafs lesm hon
            item['total']=item['price']*item['qty']
            yield item # like return final price

    def get_total(self):

        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def delete(self, product):

        product_id = str(product)

        if product_id in self.cart:

            del self.cart[product_id]

        self.session.modified = True



    def update(self, product, qty):

        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:

            self.cart[product_id]['qty'] = product_quantity

        self.session.modified = True

