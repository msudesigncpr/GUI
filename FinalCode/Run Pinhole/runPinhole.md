# Run Pin Hole Method
Hithin the colonyPickingRobot.py, below running the GUI:
> #open GUI
    app = CPR_GUI.tkinterApp()
    app.mainloop()
    runName, names, dwell, num = app.returnValues()
    print(runName, names, dwell, num)
    
There is this #Manually set calibration- that will set any offsets:
 >   #Manually set calibration
    baseplateOffsetX = 15560    #move to constants
    baseplateOffsetY = 125940   #move to constants
    CPRmotorctrl.calibrate(drive_ctrl, baseplateOffsetX, baseplateOffsetY)

To "turn on" the pinhole method, uncomment and make these changes below:
  >  #Image pinhole
    print("Starting pinhole cycle")
    pinHole = "pinHolePhoto"
    os.makedirs(pinHole)
    asyncio.run(CPRmotorctrl.pinhole(drive_ctrl, pinHole))
    offsetX, offsetY = cpr.pinhole('./pinHolePhoto/pinhole.jpg', save_image_path= './pinHolePhoto/pinhole.jpg', row_deviation_threshold=.1, column_deviation_threshold=.1, center_point=(0.5, 0.48))
    if(offsetX < 1):
        baseplateOffsetX += offsetX
        CPRmotorctrl.calibrate(drive_ctrl, baseplateOffsetX, baseplateOffsetY)
    if(offsetY < 1):
        baseplateOffsetY += offsetY
        CPRmotorctrl.calibrate(drive_ctrl, baseplateOffsetX, baseplateOffsetY)


   ... rest of code