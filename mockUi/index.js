$(() => {

    async function main() {
        console.log('main');
        let options = await getToken();
        initCatalog(options)
    }

    main();
});
