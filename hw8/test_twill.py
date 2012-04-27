import twill

twill.execute_file("test_create_user.twill", initial_url="http://localhost:8008")
twill.execute_file("test_add_message.twill", initial_url="http://localhost:8008")
twill.execute_file("test_delete_message.twill", initial_url="http://localhost:8008")
twill.execute_file("test_reply.twill", initial_url="http://localhost:8008")
twill.execute_file("test_SAM.twill", initial_url="http://localhost:8008")
twill.execute_file("test_logout.twill", initial_url="http://localhost:8008")
