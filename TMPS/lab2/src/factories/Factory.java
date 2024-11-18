package src.factories;

import src.factories.common.*;

class Factory {
    public Animal createAnimal(String animalType) {
        if (animalType.equalsIgnoreCase("dog")) {
            return new Dog();
        } else if (animalType.equalsIgnoreCase("cat")) {
            return new Cat();
        }
        return null;
    }

    public Plant createPlant(String plantType) {
        if (plantType.equalsIgnoreCase("tree")) {
            return new Tree();
        } else if (plantType.equalsIgnoreCase("flower")) {
            return new Flower();
        }
        return null;
    }
}