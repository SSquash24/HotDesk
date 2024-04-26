# Hot Desking Frontend

The frontend now communicates with the api, so if you are running it, you will not be able to get past the login screen unless you also run the api (currently in the backend branch)

## Setup

1. Install [npm](https://www.npmjs.com/package/npm) - I'm using version 10.2.4
2. In the frontend folder, run `npm install`

> [!NOTE]
> If npm lists security vulnerabilities, thats currently expected (the vulnerabilities should dissapear in the production server)

## Starting the frontend

  Start the server in development mode with `npm start` in the frontend folder

## Testing

1. To run all current tests run `npm test` in the frontend folder. They should currently all pass
2. To add new tests, write them in a new or existing _.test.js file.

> [!NOTE]
> When running tests, you may get a warning about updates not being wrapped in an act(...).
> This comes from setting up mock responses to the api calls, and I have not been able to remove them.
> The tests still all run correctly.
> To hide these warnings, you can run `npm test -- --silent` instead

## Deployment

1. Create a production build with `npm run build` (in the frontend folder).
2. Run this build with `serve -s build`

> [!IMPORTANT]
> By default, the server's api path is set to `localhost:8000`, so only the device that is running the server can see the frontend correctly. You may wish to fix this by setting `path` to the server's ip address in config.js.
