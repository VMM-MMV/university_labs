package src.notfactories.interfaces;

@FunctionalInterface
public interface ObjectFactory<T> {
    T createObject();
}