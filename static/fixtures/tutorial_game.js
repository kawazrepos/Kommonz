enchant();                                                      // ���C�u�������g�p���邽�߂̏����������F�K���ŏ��ɌĂяo���B���܂��Ȃ��̂悤�Ȃ���

window.onload = function() {
    var game = new Game(320, 320);                              // �Q�[����ʂ�320�~320�ō��BGame�̓Q�[���S�̂̏����i���C�����[�v��V�[���J�ځj���Ǘ�����N���X�B
    game.fps = 30;                                              // FPS��30�ɐݒ�B�p�b�P�[�W�̃T���v���ł̓f�t�H���g��24
    game.score = 0;                                             // �X�R�A�p�̕ϐ����`
    game.keybind(90, 'a');                                      // A�{�^����Z�L�[�ɐݒ�(����͕s�g�p)
    game.preload('miku.gif', 'map.gif', 'bullet.png');          // �Q�[�����g�p����摜�����炩���ߓǂݍ���ł���
    
    game.onload = function() {
        var miku = new Sprite(44, 32);                          // �摜�\���@�\���������I�u�W�F�N�g(Sprite)�𐶐�
        miku.x = 138;                                           // �\���ʒu���w��
        miku.y = 288;                                           // = 320 - 32
        miku.speed = 0;                                         // miku�̈ړ����x[pixel/frame]���`�B
        miku.image = game.assets['miku.gif'];                   // �\���Ɏg���摜��ݒ�
        miku.pose = 0;                                          // �A�j���[�V�����Ɏg���ϐ�
        
        // �C�x���g���X�i�܂Ƃ� : http://techblog.55w.jp/?p=473
        miku.addEventListener('enterframe', function() {        // ���t���[����������C�x���g�Ɏg���֐����`
            // ���͂ɂ���ē���������
            this.speed = 0;
            if (game.input.left) {
                this.scaleX = 1;                               	// ���E���]�\��������
                this.speed = -5;
            } else if (game.input.right) {
                this.scaleX = -1;                               // ���E���]�\��������
                this.speed = 5;
            }
        
            // �A�j���[�V�����̍X�V:�ړ���3�t���[�����ƂɁB
            if (game.frame % 4 == 0) {
                if (this.speed != 0) {
                    this.pose++;
                    this.pose %= 2;
                    this.frame = this.pose + 1;
                } else {
                    this.frame = 0;
                }
            }
            
            // �ʒu�̍X�V
            this.x += this.speed;
        });
        game.rootScene.addChild(miku);                          // �V�[���ɒǉ�����B�i���Ȃ��ƕ\������Ȃ��̂Œ��Ӂj
        
        var items = new Array();
        var itemNum = 5;
        for (i = 0; i < itemNum; i++) {
            var item = new Sprite(24, 24);                      // miku�Ɠ��l��Sprite�Ƃ��Đ���
            item.x = 32 + i * 64;
            item.y = -64;
            item.speed = 5;
            item.image = game.assets['bullet.png'];
            item.se = enchant.Sound.load('item.mp3', 'audio/mp3');
            item.se.volume = 0.5;
            item.addEventListener('enterframe', function() {
                // �ʒu�̍X�V
                this.y += this.speed;
                
                // miku�Ɠ����邩�A���܂ōs�����猳�̈ʒu�ɖ߂�
                if (this.intersect(miku)) {
                    this.se.play();
                    game.score += 100;
                    this.y = -64;
                } else if (this.y > 320) {
                    this.y = -64;
                }
            });
            
            game.rootScene.addChild(item);
        }
        
        var score = new Label();
        score.font = "12px 'Arial Black'";                      // �t�H���g�̎w��
        score.addEventListener('enterframe', function() {
            this.text = "Score : " + game.score;
        });
        
        var clearLogo = new Label("Clear !!");                  // �N���A���ɕ\�����镶��
        clearLogo.font = "24px 'Arial Black'";
        clearLogo.y = 160;
        clearLogo._element.style.textAlign = "center";          // CSS�Œ�����������
        game.addEventListener('enterframe', function() {
            if (this.score >= 2000) {
                game.rootScene.addChild(clearLogo);             // �N���A���ɕ������\������鏈�����C�x���g�ɒǉ�
            }
        });
        
        game.rootScene.addChild(score);
        game.rootScene.backgroundColor = 'rgb(182, 255, 255)';  // �w�i�F�̐ݒ�
    }
    game.start();                                               // �Q�[���N��
}
