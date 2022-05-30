async function initCart(options) {
    let token = options.token;

    let response = await fetch(getCartListUrl, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `token ${token}`
        }
    })

    let cartsData = await response.json();

    $('.total-in-cart').text(`$${cartsData.sum}`);

    let cartTable = $('#cartContainer').dxDataGrid({
        dataSource: [],
        showBorders: true,
        height: 300,
        columns: [{
            dataField: 'product.name',
            caption: 'name',
            alignment: 'center'
        }, {
            dataField: 'product.code',
            width: 90,
            caption: 'code',
            alignment: 'center'
        }, {
            dataField: 'count',
            width: 90,
            alignment: 'right',
            caption: 'count',
        }, {
            dataField: 'price',
            alignment: 'right',
            caption: 'price',
            width: 120
        }, {
            dataField: 'sum',
            caption: 'sum',
            alignment: 'right',
            width: 80
        }, {
            caption: '',
            alignment: 'center',
            width: 60,
            cellTemplate(container, options) {
                $(container).addClass('hover-btn');
                let item = $('<i class="dx-icon-close"></i>');
                container.on('click', function () {
                    addToCart(options.key)
                })
                container.append(item)
            },
        }
        ],
    }).dxDataGrid('instance');

    $('#cartList').dxList({
        dataSource: cartsData.carts,
        height: '100%',
        itemTemplate(data) {
            const result = $('<div>').addClass('cart-list__item');
            $('<div>').addClass('cart-list__item__id').text(`ID ${data.id}`).appendTo(result);
            let rightCont = $('<div>');
            $('<div>').addClass('cart-list__item__price').text(`$ ${data.order_sum}`).appendTo(rightCont);
            $('<div>').addClass('cart-list__item__supplier').text(`${data.seller.name}`).appendTo(rightCont);
            rightCont.appendTo(result);
            return result;
        },
        onItemClick: function(options) {
            getCartDetail(options.itemData.id)
        }
    }).dxList('instance');



    async function getCartDetail(id) {
        let cartData = await customFetch({
            'url': `${getCartDetailUrl}?order_id=${id}`,
            'token': token
        })
        cartTable.option('dataSource', cartData.items);
        return cartData
    }

}