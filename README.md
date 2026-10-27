## PyVOS
<p align="center">
  <strong>A Python-based operating-system experiment inspired by Android, Linux, and desktop operating systems.</strong>
</p>
<p align="center">
  <em>Driven by science, fueled by curiosity.</em>
</p>
-------------------------------------------------------------------------------------------------------------------------------------

## **About**

PyVOS is an experimental operating-system project built primarily with Python and PySide6.
The goal is to explore how an operating system can manage applications, windows, user interfaces, system services, and communication between processes — while providing applications with a PyVOS-specific API.
PyVOS takes inspiration from concepts found in Android and desktop operating systems. It is a work in progress, built as a learning and software-engineering project.

**Development status: _Experimental / under active development. PyVOS is not a production-ready operating system._**
## **Main ideas**
**Application lifecycle:** _Applications are started and managed through an Activity Manager._

**Window management:** _A Window Manager Service (WMS) coordinates application windows and UI operations._

**PyVOS API:** _Applications use PyVOS-provided interfaces instead of directly controlling the system UI._

**Runtime separation:** _Application code is executed through a dedicated runtime._

**Inter-process communication:** _BinderIPC is being developed to let application-side code communicate with system-side services._

**Restricted imports:** _The runtime includes a SafeImporter mechanism to restrict access to selected Python modules._

## **Architecture**
The application launch flow is designed around the following components:

          User / Home Screen
                  |
                  v
       Window Manager Service
                 (WMS)
                  |
                  v
       Activity Manager Service
                 (AMS)
                  |
                  v
             AppProcess
                  |
                  v
               Runtime
                  |
          +-------+-------+
          |               |
          v               v
      BinderProxy     SafeImporter
          |
          v
       BinderIPC
          |
          v
    System-side services
          |
          v
     Window Manager
          |
          v
       PySide6 UI

This represents the intended application flow and the roles of the main components; implementation details are still evolving.

## Core Components

| Component | Responsibility |
|:---|:---|
| **WMS** | Coordinates windows and UI-related operations. |
| **ActivityManagerService** | Starts and manages application activities. |
| **AppProcess** | Provides the application process/execution layer. |
| **Runtime** | Runs application code with the PyVOS runtime environment. |
| **BinderProxy** | Provides the application-side interface for system communication. |
| **BinderIPC** | Carries requests and responses between application and system components. |
| **SafeImporter** | Controls which Python modules application code can import. |
| **PyVOS API** | Provides application-facing interfaces such as UI widgets. |

## **Technology**
|||
|:---|:---|
| **Python** | _primary programming language_ |
|**PySide6 / Qt** | _graphical user interface_ |
|**BinderIPC** | _project-specific inter-process communication mechanism_ |
|**Multiprocessing / process management** | _application execution experiments_ |

## **Project structure**
The project is organized around system components, framework APIs, and the application runtime. Some important areas include:

    PyVOS/
    ├── Frameworks/
    │   └── API/
    │       └── pyvos/
    │           └── ui/
    ├── PyVOSRT/
    ├── SystemComponents/
    └── kernal/
    

The codebase is under active development, so names and locations may change. This is an overview of important areas, not an exhaustive file listing.

## **Current development**
PyVOS is being developed incrementally. Work so far includes experiments and implementation around:
* Window Manager Service and UI handling
* Application launching through ActivityManagerService
* Activity-based application structure
* Application runtime and restricted imports
* BinderProxy and BinderIPC request/response communication
* PyVOS UI widgets backed by PySide6
  
Not every planned feature is complete, and some parts of the architecture are still being refined.

## **Roadmap**
Planned areas of development include:
[1] Complete and stabilize BinderIPC
[2] Improve application lifecycle management
[3] Expand the PyVOS UI API and widget system
[4] Improve runtime isolation and error handling
[5] Develop the home screen and system UI
[6] Add built-in applications and system utilities
[7] Improve settings, themes, and file management
[8] Add documentation and developer examples

## **Running PyVOS**
PyVOS is currently a development project, and its setup and launch process may change as the architecture evolves.
For now, clone the repository:
```
    git clone https://github.com/DARK-SIDE-SCIENCE/PyVOS.git
    cd PyVOS
```
Use a Python environment with the project's required dependencies installed. Check the source code for the current entry point and dependency requirements; setup instructions will be expanded as the project becomes more stable.

## **Contributing**
Suggestions, bug reports, and ideas are welcome.
If you want to contribute:
Fork the repository.
Create a branch for your changes.
Make and test your changes.
Open a pull request describing what you changed and why.
Please remember that PyVOS is experimental. Architecture and APIs may change as development continues.

## **License**
A license has not yet been specified. Until a license is added to this repository, do not assume that the code is available for unrestricted reuse, modification, or redistribution.
---
<p align="center">
  <strong>PyVOS — exploring operating-system concepts, one component at a time.</strong>
</p>
