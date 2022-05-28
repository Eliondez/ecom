$(() => {
    DevExpress.localization.locale('ru');

    function isNotEmpty(value) {
        return value !== undefined && value !== null && value !== '';
    }

    let customDataSource = new DevExpress.data.CustomStore({
        key: "id",
        load: function (loadOptions) {
            var d = $.Deferred();
            var params = {};
            [
                "filter",
                "group",
                "groupSummary",
                "parentIds",
                "requireGroupCount",
                "requireTotalCount",
                "searchExpr",
                "searchOperation",
                "searchValue",
                "select",
                "sort",
                "skip",
                "take",
                "totalSummary",
                "userData"
            ].forEach(function (i) {
                if (i in loadOptions && isNotEmpty(loadOptions[i])) {
                    params[i] = JSON.stringify(loadOptions[i]);
                }
            });

            $.getJSON("gis_meteo/api/get_last/", params)
                .done(function (response) {
                    d.resolve(response.data, {
                        totalCount: response.totalCount,
                        summary: response.summary,
                        groupCount: response.groupCount
                    });
                })
                .fail(function () {
                    throw "Data loading error"
                });
            return d.promise();
        },
    });

    $("#dataGridContainer").dxDataGrid({
        dataSource: customDataSource,

    });

    $('#gridContainer').dxDataGrid({
        dataSource: customDataSource,
        paging: {
            pageSize: 20,
        },
        // pager: {
        //     showPageSizeSelector: true,
        //     allowedPageSizes: [10, 25, 50, 100],
        // },
        remoteOperations: {
            grouping: true
        },
        groupPanel: {visible: true},
        grouping: {
            autoExpandAll: false,
        },
        allowColumnReordering: false,
        rowAlternationEnabled: true,
        showBorders: true,
        columns: [
            {
                dataField: 'id',
                allowGrouping: false,
            },
            {
                dataField: 'date_observation',
                caption: 'date_observation',
                dataType: 'date',
            },
            {
                dataField: 'time_observation',
                caption: 'time_observation',
                allowGrouping: false,
            },
            {
                dataField: 'value',
                allowGrouping: false,
            },
        ],
        onContentReady(e) {
            if (!collapsed) {
                collapsed = true;
                e.component.expandRow(['EnviroCare']);
            }
        },
    });
});

const discountCellTemplate = function (container, options) {
    $('<div/>').dxBullet({
        onIncidentOccurred: null,
        size: {
            width: 150,
            height: 35,
        },
        margin: {
            top: 5,
            bottom: 0,
            left: 5,
        },
        showTarget: false,
        showZeroLevel: true,
        value: options.value * 100,
        startScaleValue: 0,
        endScaleValue: 100,
        tooltip: {
            enabled: true,
            font: {
                size: 18,
            },
            paddingTopBottom: 2,
            customizeTooltip() {
                return {text: options.text};
            },
            zIndex: 5,
        },
    }).appendTo(container);
};

let collapsed = false;
