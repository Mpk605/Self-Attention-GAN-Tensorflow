from SAGAN import SAGAN
import argparse
from utils import *

"""parsing and configuration"""
def parse_args():
    desc = "Tensorflow implementation of Self-Attention GAN"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--phase', type=str, default='train', help='train or test ?')
    parser.add_argument('--dataset', type=str, default='Rainbow', help='[mnist / cifar10 / celebA]')


    parser.add_argument('--epoch', type=int, default=10, help='The number of epochs to run')
    parser.add_argument('--iteration', type=int, default=50000, help='The number of training iterations')
    parser.add_argument('--batch_size', type=int, default=32, help='The size of batch per gpu')
    parser.add_argument('--print_freq', type=int, default=500, help='The number of image_print_freqy')
    parser.add_argument('--save_freq', type=int, default=500, help='The number of ckpt_save_freq')


    parser.add_argument('--g_lr', type=float, default=0.0001, help='learning rate for generator')
    parser.add_argument('--d_lr', type=float, default=0.0004, help='learning rate for discriminator')
    parser.add_argument('--beta1', type=float, default=0.0, help='beta1 for Adam optimizer')
    parser.add_argument('--beta2', type=float, default=0.9, help='beta2 for Adam optimizer')


    parser.add_argument('--z_dim', type=int, default=64, help='Dimension of noise vector')
    parser.add_argument('--sn', type=str2bool, default=True, help='using spectral norm')
    parser.add_argument('--gan_type', type=str, default='hinge', help='[gan / lsgan / wgan-gp / wgan-lp / dragan / hinge]')
    parser.add_argument('--ld', type=float, default=10.0, help='The gradient penalty lambda')
    parser.add_argument('--n_critic', type=int, default=1, help='The number of critic')

    parser.add_argument('--img_size', type=int, default=64, help='The size of image')
    parser.add_argument('--sample_num', type=int, default=30, help='The number of sample images')


    parser.add_argument('--test_num', type=int, default=10, help='The number of images generated by the test')


    parser.add_argument('--checkpoint_dir', type=str, default='drive/My Drive/SkinAI/checkpoint',
                        help='Directory name to save the checkpoints')
    parser.add_argument('--result_dir', type=str, default='drive/My Drive/SkinAI/results',
                        help='Directory name to save the generated images')
    parser.add_argument('--log_dir', type=str, default='drive/My Drive/SkinAI/logs',
                        help='Directory name to save training logs')
    parser.add_argument('--sample_dir', type=str, default='drive/My Drive/SkinAI/samples',
                        help='Directory name to save the samples on training')

    return check_args(parser.parse_args())

"""checking arguments"""
def check_args(args):
    # --checkpoint_dir
    check_folder(args.checkpoint_dir)

    # --result_dir
    check_folder(args.result_dir)

    # --result_dir
    check_folder(args.log_dir)

    # --sample_dir
    check_folder(args.sample_dir)

    # --epoch
    try:
        assert args.epoch >= 1
    except:
        print('number of epochs must be larger than or equal to one')

    # --batch_size
    try:
        assert args.batch_size >= 1
    except:
        print('batch size must be larger than or equal to one')
    return args


"""main"""
def main():
    # parse arguments
    args = parse_args()
    if args is None:
      exit()

    # open session
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
        gan = SAGAN(sess, args)

        # build graph
        gan.build_model()

        # show network architecture
        show_all_variables()

        if args.phase == 'train' :
            # launch the graph in a session
            gan.train()

            # visualize learned generator
            gan.visualize_results(args.epoch - 1)

            print(" [*] Training finished!")

        if args.phase == 'test' :
            gan.test()
            print(" [*] Test finished!")

if __name__ == '__main__':
    main()
