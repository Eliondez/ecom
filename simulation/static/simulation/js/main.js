const carCanvas = document.getElementById("carCanvas");
carCanvas.width = 300;
const networkCanvas = document.getElementById("networkCanvas");
networkCanvas.width = 500;

const carCtx = carCanvas.getContext("2d");
const networkCtx = networkCanvas.getContext("2d");

const road = new Road(
    carCanvas.width / 2,
    carCanvas.width * 0.9,
    laneCount = 5
);

const N = 100;
const cars = generateCars(N);
let bestCar = cars[0];
if (localStorage.getItem("bestBrain")) {
    for (let i = 0; i < cars.length; i++) {
        cars[i].brain = JSON.parse(
            localStorage.getItem("bestBrain"));
        if (i !== 0) {
            NeuralNetwork.mutate(cars[i].brain, 0.3);
        }
    }
}


const traffic = [
    new Car({x: road.getLaneCenter(3), y: -100, color: getRandomColor()}),
    new Car({x: road.getLaneCenter(2), y: -200, color: getRandomColor()}),
    new Car({x: road.getLaneCenter(1), y: -300, color: getRandomColor()}),

    new Car({x: road.getLaneCenter(3), y: -200, color: getRandomColor()}),
    new Car({x: road.getLaneCenter(2), y: -400, color: getRandomColor()}),
    new Car({x: road.getLaneCenter(1), y: -500, color: getRandomColor()}),
]

animate();

function save() {
    localStorage.setItem("bestBrain",
        JSON.stringify(bestCar.brain));
}

function discard() {
    localStorage.removeItem("bestBrain");
}

function generateCars(N) {
    const cars = [];
    for (let i = 1; i <= N; i++) {
        cars.push(new Car(
            {
                x: road.getLaneCenter(3),
                y: 100,
                controlType: "AI",
                maxSpeed: 3,
                color: "blue"
            }));
    }
    return cars;
}

function animate(time) {
    for (let i = 0; i < traffic.length; i++) {
        traffic[i].update(road.borders, []);
    }
    for (let i = 0; i < cars.length; i++) {
        cars[i].update(road.borders, traffic);
    }
    bestCar = cars.find(
        c => c.y === Math.min(
            ...cars.map(c => c.y)
        ));

    carCanvas.height = window.innerHeight;
    networkCanvas.height = window.innerHeight;

    carCtx.save();
    carCtx.translate(0, -bestCar.y + carCanvas.height * 0.7);

    road.draw(carCtx);
    for (let i = 0; i < traffic.length; i++) {
        traffic[i].draw(carCtx);
    }
    carCtx.globalAlpha = 0.2;
    for (let i = 0; i < cars.length; i++) {
        cars[i].draw(carCtx);
    }
    carCtx.globalAlpha = 1;
    bestCar.draw(carCtx, true);

    carCtx.restore();

    networkCtx.lineDashOffset = -time / 50;
    Visualizer.drawNetwork(networkCtx, bestCar.brain);
    // requestAnimationFrame(animate);
    setTimeout(animate, 5)
}