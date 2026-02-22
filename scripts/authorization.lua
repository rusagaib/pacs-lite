function IncomingHttpRequestFilter(method, uri, ip, username, httpHeaders)
	-- 1. Jika Admin: Beri akses penuh
	if username == "admin" then
		return true
	end

	-- 2. Jika Dokter: Bisa View, Download (GET) dan Share/Send (POST)
	if username == "dokter" then
		if method == "GET" or method == "POST" then
			return true
		else
			return false -- Blokir DELETE atau PUT (modifikasi)
		end
	end

	-- 3. Jika General: Hanya bisa View & Download (Hanya GET)
	if username == "general" then
		if method == "GET" then
			return true
		end
		-- POST HANYA untuk pencarian (Search/Find)
		if method == "POST" and (uri == "/tools/find" or string.find(uri, "/find")) then
			return true
		end

		return false -- Blokir POST, DELETE, PUT
	end

	-- 4. Jika user tidak dikenal: Tolak semua
	return false
end
