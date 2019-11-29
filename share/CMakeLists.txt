add_subdirectory(cmake)

if(NOT CMAKE_INSTALL_PREFIX STREQUAL TRIQS_ROOT)

  configure_file(triqs_hubbardi.modulefile.in triqs_hubbardi.modulefile @ONLY)
  configure_file(triqs_hubbardivars.sh.in triqs_hubbardivars.sh @ONLY)

  install(
    FILES
      ${CMAKE_CURRENT_BINARY_DIR}/triqs_hubbardi.modulefile
      ${CMAKE_CURRENT_BINARY_DIR}/triqs_hubbardivars.sh
    DESTINATION share
  )
 
  message(STATUS "***************************************************************")
  message(STATUS "* Custom install Location. Use:                                ")
  message(STATUS "*                                                              ")
  message(STATUS "*   source ${CMAKE_INSTALL_PREFIX}/share/triqs_hubbardivars.sh      ")
  message(STATUS "*                                                              ")
  message(STATUS "* to set up the environment variables                          ")
  message(STATUS "***************************************************************")

endif()
