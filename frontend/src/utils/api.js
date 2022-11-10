import axios from "axios";

const BACKEND_SERVER = `${process.env.REACT_APP_BACKEND_HOST}:${process.env.REACT_APP_BACKEND_PORT}/api/ver1.0/`;

// Get request with authentication
export async function authGet(route, payload = {}) {
    return axios.get(`http://${BACKEND_SERVER}${route}`, {
        ...payload,
    });
}

// Post request with authentication
export async function authPost(route, payload = {}) {
    return axios.post(`http://${BACKEND_SERVER}${route}`, {
        ...payload,
    });
}

// Put request with authentication
export async function authPut(route, payload = {}) {
    return axios.put(`http://${BACKEND_SERVER}${route}`, {
        ...payload,
    });
}

// Delete request with authentication
export async function authDelete(route, payload = {}) {
    return axios.delete(`http://${BACKEND_SERVER}${route}`, {
        ...payload,
    });
}

/* USAGE EXAMPLE

api.authPost('shift/', {
    start_timestamp : x, end_timestamp : x,  number_of_workers: x,  workstation: x,
  })
.then((res) => {
    // Handle OK response
})
.catch((err) => {
    // Handle error response
});

*/

const api = {
    authGet,
    authPost,
    authPut,
    authDelete,
};

export default api;
