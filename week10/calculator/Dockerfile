# Build the jar with the project's Gradle wrapper (Gradle 4.10.2) on JDK 8.
# The wrapper pins the Gradle version, so only the JDK has to match the project.
FROM eclipse-temurin:8-jdk AS build
WORKDIR /src

# 1. Copy the script AND the complete wrapper directory structure
COPY gradlew .
COPY gradle/wrapper/ gradle/wrapper/

# 2. Download and cache the Gradle distribution binaries (Now works perfectly)
RUN chmod +x gradlew && ./gradlew --version --no-daemon

# 3. Copy the rest of your Java source code
COPY . .

# 4. Compile the jar
RUN ./gradlew bootJar --no-daemon

# Run it on a small JRE. Spring Boot listens on 8080.
FROM eclipse-temurin:8-jre
COPY --from=build /src/build/libs/*.jar /app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
