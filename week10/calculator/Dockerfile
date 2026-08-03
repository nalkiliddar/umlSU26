# Build the jar with the project's Gradle wrapper (Gradle 4.10.2) on JDK 8.
# The wrapper pins the Gradle version, so only the JDK has to match the project.
FROM eclipse-temurin:8-jdk AS build
WORKDIR /src

# Copy all repository contents (including the local gradle zip file)
COPY . .

# Run the compilation. It will instantly unpack the local zip file without internet traffic!
RUN chmod +x gradlew && ./gradlew bootJar --no-daemon

# Run it on a small JRE. Spring Boot listens on 8080.
FROM eclipse-temurin:8-jre
COPY --from=build /src/build/libs/*.jar /app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
