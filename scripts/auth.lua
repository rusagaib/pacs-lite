local jwt = require 'resty.jwt'  -- pastikan LuaJIT + lua-resty-jwt tersedia
local cjson = require 'cjson'

-- load public key Authentik
local public_key = [[
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqh...
-----END PUBLIC KEY-----
]]

function orthanc_auth()
    local token = ngx.var.http_x_auth_token
    if not token then
        return ngx.exit(401)
    end

    local jwt_obj = jwt:verify(public_key, token)
    if not jwt_obj.verified then
        return ngx.exit(401)
    end

    local groups = jwt_obj.payload.groups
    local role = "Read"

    if groups["admin_group"] then
        role = "OrthancAdministrator"
    elseif groups["dokter_group"] then
        role = "ReadWrite"
    elseif groups["radiologi_group"] then
        role = "Read"
    end

    ngx.req.set_header("X-Orthanc-UserRole", role)
    ngx.req.set_header("X-Orthanc-Username", jwt_obj.payload.preferred_username)
end

