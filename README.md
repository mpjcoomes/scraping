# scraping

Financial websites have strict Terms of Service regarding how they are accessed. As such, any web scraping program should be designed to use the website no more aggressively than a real human would. This approach means that code takes a long time to run. However, it prevents your activities from causing damage, or being viewed as causing damage.

This program touches the ASX website, just once, to download a public list of financial products. As such, it replicates a normal fair-use human interaction.

After that, it very slowly (i.e. 10 seconds between pages) crawls through a financial website to left-join additional information. Effectively, this slow approach replicates a human copying the ASX list into a spreadsheet, then systematically going through each product to add useful information.

This slow fair-use approach requires ~36.5 minutes.
