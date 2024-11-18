package src.factories;

import src.factories.common.Animal;
import src.factories.common.Plant;

public class Main {
    public static void main(String[] args) {
        // Normal Factory
        Factory factory = new Factory();

        Animal dog = factory.createAnimal("dog");
        dog.makeSound();

        Animal cat = factory.createAnimal("cat");
        cat.makeSound();

        Plant tree = factory.createPlant("tree");
        tree.grow();

        Plant flower = factory.createPlant("flower");
        flower.grow();

        // Abstract Factory
        AbstractFactory factoryOne = new AbstractFactoryOne();
        AbstractFactory factoryTwo = new AbstractFactoryTwo();

        Animal forestAnimal = factoryOne.createAnimal();
        Plant forestPlant = factoryOne.createPlant();

        Animal gardenAnimal = factoryTwo.createAnimal();
        Plant gardenPlant = factoryTwo.createPlant();

        forestAnimal.makeSound();
        forestPlant.grow();

        gardenAnimal.makeSound();
        gardenPlant.grow();
    }
}