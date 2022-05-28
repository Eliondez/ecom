
function generateRoad(options) {
    let gameContainer = options.gameContainer;
    const linesNum = options.linesNum || 1;
    const roadOffsetX = options.roadOffsetX || 0;
    const roadOffsetY = options.roadOffsetY || 0;
    const roadLength = options.roadLength || 1500;
    const lineWidth = options.lineWidth || 11;

    const bordersWidth = options.bordersWidth || 2;
    const roadWidth = bordersWidth * 2 + linesNum * lineWidth + (linesNum - 1);
    const leftBorderX = roadOffsetX;
    const rightBorderX = roadOffsetX + roadWidth - bordersWidth;
    const borderColor = 0x666666;
    const lineColor = 0x555555;

    let roadBackground = new PIXI.Sprite(PIXI.Texture.WHITE);
    roadBackground.tint = 0x333333;
    roadBackground.x = leftBorderX;
    roadBackground.y = roadOffsetY;
    roadBackground.width = rightBorderX - leftBorderX;
    roadBackground.height = roadLength;
    gameContainer.addChild(roadBackground);

    let leftBorder = new PIXI.Sprite(PIXI.Texture.WHITE);
    leftBorder.tint = borderColor;
    leftBorder.x = leftBorderX;
    leftBorder.y = roadOffsetY;
    leftBorder.width = bordersWidth;
    leftBorder.height = roadLength;
    gameContainer.addChild(leftBorder);

    let rightBorder = new PIXI.Sprite(PIXI.Texture.WHITE);
    rightBorder.tint = borderColor;
    rightBorder.x = rightBorderX;
    rightBorder.y = roadOffsetY;
    rightBorder.width = bordersWidth;
    rightBorder.height = roadLength;
    gameContainer.addChild(rightBorder);

    let res = {
        linesNum: linesNum,
        lineWidth: lineWidth,
        roadOffsetX: roadOffsetX,
        roadOffsetY: roadOffsetY,
        roadLength: roadLength,
        leftBorderX: leftBorderX,
        rightBorderX: rightBorderX,
        lines: []
    }
    res.lines.push(leftBorderX + bordersWidth);
    for (let i = 1; i < linesNum; i++) {
        let x = leftBorderX + bordersWidth + i * lineWidth + i;
        let sprite = new PIXI.Sprite(PIXI.Texture.WHITE);
        sprite.tint = lineColor;
        sprite.x = x;
        sprite.y = 0;
        sprite.width = 1;
        sprite.height = 1500;
        gameContainer.addChild(sprite);
        res.lines.push(x);
    }
    return res
}