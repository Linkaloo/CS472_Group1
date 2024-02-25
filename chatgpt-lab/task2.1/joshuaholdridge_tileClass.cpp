class Tile
{
public:
    Tile(){};
    Tile(int, int, int);
    Tile(int, int, int, sf::Sprite);
    Tile(int, int, int, sf::IntRect, sf::Texture &);
    ~Tile(){};

private:
    sf::Texture *texture;
    sf::Sprite shape;
    int size;
    int gridX;
    int gridY;

    void initialize(int x, int y, int tileSize, sf::Sprite *sprite = nullptr, 
                    sf::IntRect *textureLocation = nullptr, sf::Texture *textureFile = nullptr);
}

void Tile::initialize(int x, int y, int tileSize, sf::Sprite *sprite = nullptr, 
                sf::IntRect *textureLocation = nullptr, sf::Texture *textureFile = nullptr)
{
    this->gridX = x;
    this->gridY = y;
    this->size = tileSize;

    if(sprite != nullptr) {
        this->shape = *sprite;
    }

    if(textureFile != nullptr && textureLocation != nullptr) {
        this->shape.setTexture(textureFile);
        this->shape.setTextureRect(textureLocation);
        this->shape.setPosition(this->gridX, this->gridY);
    }
}

Tile::Tile(int x, int y, int tileSize)
{
    initialize(x, y, tileSize);
}

Tile::Tile(int x, int y, int tileSize, sf::Sprite sprite)
{
    initialize(x, y, tileSize, &sprite);
}

Tile::Tile(int x, int y, int tileSize, sf::IntRect textureLocation, sf::Texture &textureFile)
{
    initialize(x, y, tileSize, nullptr, &textureLocation, &textureFile);
}