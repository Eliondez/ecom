const app = new PIXI.Application({
    width: 800,
    height: 600,
    backgroundColor: 0x222222,
    resolution: window.devicePixelRatio || 1,
});
document.body.appendChild(app.view);

const gameContainer = new PIXI.Container();
gameContainer.x = 0;
gameContainer.y = 0;
app.stage.addChild(gameContainer);

let world = {};

let carsAndObjects = [];

function createCars(options) {
    let lines = options.lines;
    let lineNum = 0;
    // let carCount = 1; //options.linesNum * 3;
    let carCount = 2; //options.linesNum * 3;
    for (let i = 0; i < carCount; i++) {
        let y = 300 + i * 80;
        let x = lines[lineNum] + options.lineWidth / 2;
        // lineNum += 1;
        // if (lineNum >= options.linesNum) {
        //     lineNum = 0;
        // }

        carsAndObjects.push(new createCar({
            id: i,
            x: x,
            y: y,
            speed: 0,
            maxSpeed: 1 + i * 0.5,
            color: 0x000000,
            objectsAware: true,
            carWidth: options.lineWidth * 0.6,
            gameContainer: gameContainer,
            world: world
        }));
    }
}


let roadData = generateRoad({
    linesNum: 6,
    roadOffsetX: 250,
    lineWidth: 37,
    bordersWidth: 5,
    gameContainer: gameContainer
});

world.roadData = roadData;
createCars(roadData);

let engine = new Engine(carsAndObjects);
engine.start()

document.querySelector('.toggle-btn').addEventListener('click', function() {
    engine.toggle()
})