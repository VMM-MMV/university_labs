package src.notfactories.interfaces;

@FunctionalInterface
public interface Prototype<T> {
    T copy();
}