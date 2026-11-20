LABS = coin_flip waiting_bus binomial_poisson central_limit_theorem \
	moment_generating_functions

# make               build every lab
# make <lab>         build one lab, e.g. make coin_flip
# make run-<lab>     build and run one lab with its example arguments
# make clean         remove every built program
all: $(LABS)

$(LABS):
	$(MAKE) -C $@

run-%:
	$(MAKE) -C $* run

clean:
	@for d in $(LABS); do $(MAKE) -C $$d clean; done

re: clean all

.PHONY: all clean re $(LABS)
