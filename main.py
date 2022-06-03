import numpy as np

from numba import jit, cuda # gpu

import pygame
from vector import Vector3 as v3

pygame.init()

screen_size = 300
infoObject = pygame.display.Info()
display_w, display_h = infoObject.current_w * 0.8, infoObject.current_h * 0.8
screen_w, screen_h = screen_size, screen_size - 100
aspect_ratio = screen_w / screen_h
# aspect_ratio = screen_size / 200
# screen_w, screen_h = screen_size, 200
screen = pygame.display.set_mode((screen_w, screen_h))


def normalize(vector):
    return vector / np.linalg.norm(vector)


def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis


class Sphere:
    def __init__(self, pos, radius, ambient=np.array([0.1, 0, 0]), diffuse=np.array([0.7, 0, 0]), specular=np.array([1, 1, 1]), shininess=100, reflection=0.5):
        self.center = pos
        self.r = radius
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflection = reflection

    def intersect(self, ray_origin, ray_dir):
        # print(ray_origin)
        # input(ray_dir)
        # [-0.63960215  0.42640143 -0.63960215]

        b = 2 * np.dot(ray_dir, ray_origin - self.center)
        c = np.linalg.norm(ray_origin - self.center) ** 2 - self.r ** 2
        discriminant = b ** 2 - 4 * c
        if discriminant > 0:
            dis1 = (-b + np.sqrt(discriminant)) / 2
            dis2 = (-b - np.sqrt(discriminant)) / 2
            if dis1 > 0 and dis2 > 0:
                return min(dis1, dis2)
        return None


class Light:
    def __init__(self, pos, ambient=np.array([1, 1, 1]), diffuse=np.array([1, 1, 1]), specular=np.array([1, 1, 1])):
        self.center = pos
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular


@jit()
def nearest_intersection(scene, ray_origin, ray_dir):
    distances = [o.intersect(ray_origin, ray_dir) for o in scene]
    min_dist = 10000000000000000000000000000000000000000000000000
    nearest = None

    for i, distance in enumerate(distances):
        if distance is not None and distance < min_dist:
            min_dist = distance
            nearest = scene[i]
    return nearest, min_dist

@jit()
def render_frame(scene, camera, light, screen_r):
    image = pygame.Surface((screen_w, screen_h))
    max_depth = 3
    for i, y in enumerate(np.linspace(screen_r[1], screen_r[3], screen_h)):
        for j, x in enumerate(np.linspace(screen_r[0], screen_r[2], screen_w)):
            pixel = np.array([x, y, 0])
            origin = camera
            dir = normalize(pixel - origin)
            color = np.zeros((3))
            reflection = 1
            for k in range(max_depth):
                nearest, dist = nearest_intersection(scene, origin, dir)
                if nearest is not None:
                    intersection = origin + dir * dist
                else:
                    image.set_at((j, i), (0, 0, 0))
                    break
                normal = normalize(intersection - nearest.center)
                shifted = intersection + normal * 0.001
                to_light_dir = normalize(light.center - shifted)

                is_blocked = nearest_intersection(scene, intersection, to_light_dir)[1] < np.linalg.norm(light.center - intersection)
                if is_blocked: break

                illumination = np.zeros((3))
                illumination += nearest.ambient * light.ambient
                illumination += nearest.diffuse * light.diffuse * np.dot(to_light_dir, normal)
                h = normalize(to_light_dir + normalize(camera - intersection))
                illumination += nearest.specular * light.specular * np.dot(normal, h) ** (nearest.shininess / 4)
                color += illumination * reflection
                reflection *= nearest.reflection

                origin = shifted
                dir = reflected(dir, normal)

            image.set_at((j, i), np.clip(color, 0, 1) * 255)
        print(str(int(i + 1)) + '/' + str(screen_h))
        pygame.display.update()

    return image


def main():
    scene = [
        Sphere(np.array([-0.3, 0, -1]), 0.7, ambient=np.array([0.1, 0, 0.1]), diffuse=np.array([0.7, 0, 0.7]), specular=np.array([1, 1, 1]), shininess=100, reflection=0.5),
        Sphere(np.array([0.2, -0.2, 0]), 0.1, ambient=np.array([0.1, 0.1, 0.1]), diffuse=np.array([0.7, 0.7, 0.7]), specular=np.array([1, 1, 1]), shininess=100, reflection=0.5),
        Sphere(np.array([-0.4, 0.1, 0]), 0.15, ambient=np.array([0, 0, 0.1]), diffuse=np.array([0, 0, 0.6]), specular=np.array([1, 1, 1]), shininess=100, reflection=0.5),
        Sphere(np.array([0, -9000, 0]), 9000 - 0.7, ambient=np.array([0.1, 0.05, 0.1]), diffuse=np.array([0.6, 0.6, 0.6]), specular=np.array([1, 1, 1]), shininess=100, reflection=0.5)
    ]
    camera = np.array([0, 0, 1])
    light = Light(np.array([5, 5, 5]))
    screen_r = (-1, 1 / aspect_ratio, 1, -1 / aspect_ratio)

    running = True
    while running:
        image = render_frame(scene, camera, light, screen_r)
        screen.blit(pygame.transform.scale(image, (screen_w, screen_h)), (0, 0))
        pygame.display.update()
        input()


if __name__ == "__main__":
    main()
    pygame.quit()
