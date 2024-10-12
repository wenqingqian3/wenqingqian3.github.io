#include "blog.h"
#include "config.h"

bool IF_GEN_BLOG_INDEX_TOC;

// blog_generator_beg
extern blog blog_cate1_s1;
extern blog blog_reprint_cate1_1;
extern blog blog_reprint_cate4_3;
extern blog blog_reprint_cate5_4;
extern blog blog_cate2_redirect;
extern blog blog_cate2_language;
extern blog blog_reprint_cate2_2;

void blog_generate(){
	vector<blog> blogvec {
		blog_cate1_s1,
		blog_reprint_cate1_1,
		blog_reprint_cate4_3,
		blog_reprint_cate5_4,
		blog_cate2_redirect,
		blog_cate2_language,
		blog_reprint_cate2_2,
	};
	extern void generate_blog_index(vector<blog>&, bool);
	generate_blog_index(blogvec, IF_GEN_BLOG_INDEX_TOC);
}
// blog_generator_end

int main(int argc, char** argv)
{
	if(strcmp(argv[0], "on")) IF_GEN_BLOG_INDEX_TOC = true;
	else                      IF_GEN_BLOG_INDEX_TOC = false;

	blog_generate();
}

















































