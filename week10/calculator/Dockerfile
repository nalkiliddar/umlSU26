# Build the jar with the project's Gradle wrapper (Gradle 4.10.2) on JDK 8.
# The wrapper pins the Gradle version, so only the JDK has to match the project.
FROM eclipse-temurin:8-jdk AS build
WORKDIR /src

# 1. Copy the script and the complete wrapper directory structure
COPY gradlew .
COPY gradle/wrapper/ gradle/wrapper/

# 2. Copy ONLY your dependency build manifest files
COPY build.gradle .
COPY settings.gradle* . 

# 3. CRITICAL ACCELERATION: Fetch all plugins and jar dependencies into a cached layer
# This downloads the internet ONCE. Future builds skip this entirely.
RUN chmod +x gradlew && ./gradlew buildEnvironment dependencies --no-daemon

# 4. Copy your actual Java source code files (Frequent changes happen here)
COPY . .

# 5. Compile the jar safely (Will take seconds because everything is pre-downloaded)
RUN ./gradlew bootJar --no-daemon

# Run it on a small JRE. Spring Boot listens on 8080.
FROM eclipse-temurin:8-jre
COPY --from=build /src/build/libs/*.jar /app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
