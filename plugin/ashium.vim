py import ashium

au BufReadPost /tmp*/ash.*/* py ashium.try_to_load_from_current_file()
