-- auth-header.lua
function OnRestApiCall(method, uri, headers, body)
    local username = headers["X-Orthanc-User"]
    local password = headers["X-Orthanc-Pass"]

    if username ~= nil and password ~= nil then
        local ok = RestAuthentication(username, password)
        if ok then
            return 200, "User authenticated"
        else
            return 401, "Unauthorized"
        end
    end

    return 403, "Forbidden"
end

