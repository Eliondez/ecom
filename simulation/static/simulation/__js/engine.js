
class Engine {
    constructor(objList) {
        this.delta = 20;
        this.maxCicles = 11500;
        this.currentCicle = 0;
        this.running = false;
        this.objects = objList;
    }

    iterate() {
        this.currentCicle += 1;
        if (this.maxCicles > 0 && this.currentCicle >= this.maxCicles) {
            this.running = false;
        }
        if (!this.running) {
            return;
        }
        this.objects.forEach(item => {
            item.iterate(this.currentCicle);
        })

        setTimeout(() => this.iterate(), this.delta);
    }

    start() {
        this.currentCicle = 0;
        this.running = true;
        this.iterate();
    }

    stop() {
        this.running = false;
    }

    toggle() {
        if (this.running) {
            this.stop();
        } else {
            this.start();
        }
    }

}