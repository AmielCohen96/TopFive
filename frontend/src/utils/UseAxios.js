import {jwtDecode} from 'jwt-decode';
import dayjs from "dayjs";
import AuthContext from "../context/AuthContext.js";
import axios from "axios";
import {useContext} from "react";

const baseURL = "http://localhost:8080/";

const useAxios = () => {
    const {authTokens, setUser, setAuthTokens} = useContext(AuthContext);

    const axiosInstance = axios.create({
        baseURL: baseURL,
        headers: {Authorization: `Bearer ${authTokens.access}`}
    })
    axiosInstance.interceptors.request.use(async req => {
        const user = jwtDecode(authTokens)
        const isExpired = dayjs.unix(user.exp).diff(dayjs() < 1)

        if (isExpired) {
            return req
        }

        const response = await axios.post(${baseURL}'/token/refresh', {
            refresh: authTokens.refresh
        })
        localStorage.setItem("authToken", JSON.stringify(response.data))

        setAuthTokens(response.data)
        setUser(jwtDecode(response.data.access))

        req.headers.Authorization = `bearer ${response.data.access}`
        return req
    })

    return axiosInstance
}

export default useAxios()