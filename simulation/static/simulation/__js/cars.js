let createCar = function (options) {
    let gameContainer = options.gameContainer;
    this.car = new PIXI.Container();
    this.id = options.id;
    this.angle = 0;
    this.car.x = options.x;
    this.car.y = options.y;
    this.objectsAware = options.objectsAware;
    this.detectDistance = 100;
    this.maxSpeed = options.maxSpeed || 1 + Math.random();
    this.speed = this.maxSpeed; //options.speed;
    this.thurstPower = 0.01 + Math.random() * 0.03
    this.onThurst = false;
    this.onBrake = false;
    this.world = options.world;
    this.angleSpeed = 0.007;
    this.affectedLines = [-1, -1];

    let carWidth = options.carWidth;
    let carHeight = carWidth * 1.5;

    this.mainBody = new PIXI.Sprite(PIXI.Texture.WHITE);
    this.mainBody.tint = 0x009900;
    this.mainBody.width = carWidth;
    this.mainBody.x = -carWidth / 2;
    this.mainBody.height = carHeight;
    this.mainBody.y = -carHeight / 2;
    this.car.addChild(this.mainBody)

    this.leftBorder = new PIXI.Sprite(PIXI.Texture.WHITE);
    this.leftBorder.tint = 0x000000;
    this.leftBorder.width = 2;
    this.leftBorder.x = -carWidth / 2;
    this.leftBorder.height = carHeight;
    this.leftBorder.y = -carHeight / 2;
    this.car.addChild(this.leftBorder)

    this.rightBorder = new PIXI.Sprite(PIXI.Texture.WHITE);
    this.rightBorder.tint = 0x000000;
    this.rightBorder.width = 2;
    this.rightBorder.x = carWidth / 2 - 2;
    this.rightBorder.height = carHeight;
    this.rightBorder.y = -carHeight / 2;
    this.car.addChild(this.rightBorder)

    this.customLogic = options.customLogic;

    this.minDistance = carWidth * 2;

    this.getSpeedVector = function() {
        return {
            vx: this.speed * Math.sin(this.angle),
            vy: this.speed * Math.cos(this.angle)
        }
    }

    this.getCurrentX = function() {
        return this.car.x;
    }

    this.getTargetX = function () {
        // if (this.id === 4) {
        //     let lines = this.world.roadData.lines;
        //     let lineWidth = this.world.roadData.lineWidth;
        //     return lines[5] + lineWidth / 2;
        // }

        // if (this.id === 1) {
        //     let lines = this.world.roadData.lines;
        //     let lineWidth = this.world.roadData.lineWidth;
        //     return lines[0] + lineWidth / 2;
        // }

        return this.getCurrentX()
    }

    this.changeAngle = function(value) {
        if (this.speed < 1) {
            return
        }
        this.angle += value;
    }

    this.reduceAngleToZero = function() {
        if (Math.abs(this.angle) < this.angleSpeed * 2) {
            this.angle = 0;
        } else if (this.angle > 0) {
            this.changeAngle(-this.angleSpeed)
        } else {
            this.changeAngle(this.angleSpeed)
        }
    }

    this.adjustAngle = function() {
        const currentX = this.getCurrentX();
        const targetX = this.getTargetX();

        // if (this.id === 4) {
        //     console.log('adjustAngle', currentX, targetX, this.speed);
        // }

        let deltaX = currentX - targetX;
        if (Math.abs(deltaX) < 19) {
            this.reduceAngleToZero()
        } else {
            let changeAngleValue = deltaX > 0 ? -this.angleSpeed : this.angleSpeed;
            this.changeAngle(changeAngleValue)
        }
    }

    this.iterate = function(currentCicle) {
        this.currentCicle = currentCicle;

        if (this.objectsAware) {
            this.detectObjects();
        }

        if (this.customLogic) {
            this.customLogic(currentCicle)
        }

        if (this.onThurst) {
            this.speed = Math.min(this.maxSpeed, this.speed + this.thurstPower);
            this.onThurst = false;
        }
        if (this.onBrake) {
            this.speed = Math.max(0, this.speed - 0.7);
            this.onBrake = false;
        }
        let speedVector = this.getSpeedVector();

        this.adjustAngle()

        this.car.y -= speedVector.vy;
        this.car.x += speedVector.vx;
        this.car.rotation = this.angle;


        if (this.car.y < 0) {
            this.car.y = 700;
        }
    }

    this.thurst = function () {
        this.onThurst = true;
        this.onBrake = false;
        this.mainBody.tint = 0x008800;
    }

    this.break = function () {
        // if (this.id === 6) {
        //     console.log('break');
        // }
        this.onBrake = true;
        this.onThurst = false;
        this.mainBody.tint = 0x880000;
    }

    this.getCurrentLines = function() {
        // todo: сделать нормально с геометрией
        let leftBoundary = this.car.x - 15;
        let rightBoundary = this.car.x + 15;
        let affectedLinesStartAt = -1;
        let affectedLinesEndAt = -1;

        this.world.roadData.lines.forEach((lineStart, idx) => {
            let lineEnd = lineStart + this.world.roadData.lineWidth + 1;
            if (leftBoundary > lineStart && leftBoundary < lineEnd) {
                affectedLinesStartAt = idx;
            }
            if (rightBoundary > lineStart && rightBoundary < lineEnd) {
                affectedLinesEndAt = idx;
            }
        })
        this.affectedLines = [affectedLinesStartAt, affectedLinesEndAt];
    }

    this.calcDistance = function (entity) {
        let deltaX = this.car.x - entity.car.x;
        let deltaY = this.car.y - entity.car.y;
        let leftBlock = false;
        let rightBlock = false;
        let forwardDist = null;

        if (Math.abs(deltaX) < 50 && Math.abs(deltaY) < 60) {
            if (deltaX < 0) {
                rightBlock = true;
            } else {
                leftBlock = true;
            }
        }

        if (Math.abs(deltaX) < 35 && deltaY > 0) {
            forwardDist = deltaY;
        }

        // if (this.id === 6) {
        //     console.log('forwardDist', forwardDist);
        // }

        return {
            forwardDist: forwardDist,
            leftBlock: leftBlock,
            rightBlock: rightBlock
        }

    }
    this.detectObjects = function () {
        this.getCurrentLines()
        let minDistance = Number.MAX_VALUE;

        let leftBlock = false;
        let rightBlock = false;

        if (this.affectedLines[0] === -1 || this.affectedLines[1] === -1) {
            // console.log('Off road');
        } else {
            carsAndObjects.forEach(item => {
                if (this.id === item.id) {
                    return
                }
                let distParams = this.calcDistance(item)

                let forwardDist = distParams.forwardDist;
                if (distParams.leftBlock) {
                    leftBlock = true;
                }
                if (distParams.rightBlock) {
                    rightBlock = true;
                }
                if (forwardDist) {
                    if (forwardDist < minDistance) {
                        minDistance = forwardDist;
                    }
                }
            })
        }

        // if (this.id === 6) {
        //     console.log('minDistance', minDistance);
        // }

        if (leftBlock) {
            this.leftBorder.tint = 0x880000;
        } else {
            this.leftBorder.tint = 0x000000;
        }

        if (rightBlock) {
            this.rightBorder.tint = 0x880000;
        } else {
            this.rightBorder.tint = 0x000000;
        }

        if (minDistance <= this.minDistance) {
            this.break();
        } else {
            this.thurst();
        }
    }
    gameContainer.addChild(this.car);
    return this
}