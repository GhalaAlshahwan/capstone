# Software Requirements:
1. OpenCV + Raspberry Pi: Python. Libraries: OpenCV, Numpy.
2. Arduino: Arduino IDE (C++)
3. Backend: Node.js (Express.js) + SQLite 
4. Frontend: React (Typescript, Tailwind CSS, Vite, Shadcn)

IDEs: VSC, Arduino IDE.

   # Libraries/Tools:
   # Raspberry Pi:
      
   * OpenCV: image capture (alr did a prototype of this last sem)
      
   * Numpy: array operations (masks + color schemes -> used in last sem prototype as well)
      
   * Requests: sends HTTP req to node.js (backend) via POST
   
   
   # Backend:

   *Node.js + npm*
      
   * Express: server (handles incoming requests and responses from the request made via python)
      
   * Sqlite: stores logs locally (raspberry pi)
      
   * CORS: cross origin requests, to access a different port (Node.js backend)
      
   Installed in project folder.
     
   Data handling flow: Python script -> Node.js (reads/writes into the db) -> Sqlite (detection_log.db on Pi) -> React fetches from Node.js via API call NOT the db itself. 
   
     
   # Frontend:
      
   * React (node.js + npm)
      
   * Typescript: main logic
      
   * Tailwind CSS: styling tool
      
   * Vite: build tool
   
   * Shadcn: ui components
