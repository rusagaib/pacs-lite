local jwt = require("resty.jwt")  -- gunakan lua-resty-jwt

-- Mapping group Authentik ke role Orthanc
local role_map = {
  ["admin_group"] = "OrthancAdministrator",
  ["dokter_group"] = "ReadWrite"
}

function OnHttpRequest(request)
  local auth_header = request.Headers["Authorization"]
  if not auth_header then
    return 401, "Missing Authorization header"
  end

  local token = auth_header:match("Bearer%s+(.+)")
  if not token then
    return 401, "Invalid Authorization header"
  end

  -- Verifikasi JWT
  local jwt_obj = jwt:verify("YOUR_AUTHENTIK_PUBLIC_KEY_HERE", token)
  if not jwt_obj["verified"] then
    return 403, "Invalid token"
  end

  local claims = jwt_obj["payload"]
  if not claims or not claims["groups"] then
    return 403, "No groups in token"
  end

  -- Mapping ke role Orthanc
  local orthanc_role = "Read"  -- default
  for _, g in ipairs(claims["groups"]) do
    if role_map[g] then
      orthanc_role = role_map[g]
      break
    end
  end

  request.UserName = claims["username"] or "unknown"
  request.UserRole = orthanc_role

  -- Request diteruskan ke Orthanc
  return 0
end

