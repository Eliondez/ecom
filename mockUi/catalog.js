async function initCatalog(options) {
    let token = options.token

    const store = new DevExpress.data.CustomStore({
        key: 'id',
        load(loadOptions) {
            const deferred = $.Deferred();
            const args = {};

            let params = ['dicts=suppliers,categories'];

            let page_size = loadOptions.take;
            let page = 1 + (loadOptions.skip / page_size);
            params.push(`page_size=${page_size}`);
            params.push(`page=${page}`);

            let url = getCatalogUrl;
            if (params.length) {
                url = `${url}?${params.join('&')}`
            }

            $.ajax({
                url: url,
                dataType: 'json',
                data: args,
                success(result) {
                    let supplierDict = {};
                    result.dicts.suppliers.forEach(item => {
                        supplierDict[item.id] = item.name
                    })
                    let categoriesDict = {};
                    result.dicts.categories.forEach(item => {
                        categoriesDict[item.id] = item.name
                    })
                    let items = result.results.map(item => {
                        item.category = categoriesDict[item.category];
                        item.supplier = supplierDict[item.supplier];
                        return item
                    })
                    deferred.resolve(items, {
                        totalCount: result.count,
                    });
                },
                error() {
                    deferred.reject('Data Loading Error');
                },
                timeout: 5000,
            });

            return deferred.promise();
        },
    });

    async function addToCart(productId) {
        const response = await fetch(addToCartUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `token ${token}`
            },
            body: JSON.stringify({
                "product_id": productId,
                "count": 1
            })
        })
        const data = await response.json();
        console.log('data', data);
    }

    $('#gridContainer').dxDataGrid({
        dataSource: store,
        showBorders: true,
        remoteOperations: true,
        paging: {
            pageSize: 15,
        },
        columns: [{
            dataField: 'id',
            width: 50
        }, {
            dataField: 'code',
            width: 90,
            alignment: 'center'
        }, {
            dataField: 'category',
            alignment: 'right'
        }, {
            dataField: 'name',
            alignment: 'right',
            width: 120
        }, {
            dataField: 'current_price',
            caption: 'Price',
            alignment: 'right',
            width: 60
        }, {
            dataField: 'supplier',
            alignment: 'right',
            width: 180
        }, {
            caption: 'Cart',
            alignment: 'center',
            width: 60,
            cellTemplate(container, options) {
                $(container).addClass('hover-btn');
                let item = $('<i class="dx-icon-cart"></i>');
                container.on('click', function () {
                    addToCart(options.key)
                })
                container.append(item)
            },
        }
        ],
    }).dxDataGrid('instance');
}