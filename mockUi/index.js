$(() => {

    async function main() {
        let options = await getToken();
        initCatalog(options);
        initCart(options);
    }

    main();
});
