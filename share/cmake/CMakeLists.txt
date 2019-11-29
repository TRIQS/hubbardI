configure_file(triqs_hubbardi-config.cmake.in triqs_hubbardi-config.cmake @ONLY)
configure_file(triqs_hubbardi-config-version.cmake.in triqs_hubbardi-config-version.cmake @ONLY)
install(
  FILES
    ${CMAKE_CURRENT_BINARY_DIR}/triqs_hubbardi-config.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/triqs_hubbardi-config-version.cmake
  DESTINATION lib/cmake/triqs_hubbardi
)

install(EXPORT triqs_hubbardi-targets NAMESPACE triqs_hubbardi:: DESTINATION lib/cmake/triqs_hubbardi)
