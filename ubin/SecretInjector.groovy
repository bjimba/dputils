import groovy.text.SimpleTemplateEngine
import groovy.util.XmlSlurper;
import groovy.xml.XmlUtil;


/*		BufferedReader br = new BufferedReader(new InputStreamReader(System.in))
		print "Enter target Environment:"
		def targetEnv = br.readLine()*/
		
		
		def props = System.getProperties();
		def userDir = props.get('user.dir');
		println "userDir :"+userDir;
		def targetEnv = args[0];
		def confidentialXMLPath = args[1];
		
		println "targetEnv :"+args[0];
		println "confidentialXMLPath :"+args[1];

		def targetFilePath = null;
		def tempTargetFile = null;
		def envName = null;
		def envPath = null;
		def binding = null;


		try {
		
				//def configXML =  new XmlParser().parse("src/dpbuild/dpbuild/Confidential_DBPLRetail.xml")
				def configXML =  new XmlParser().parse(confidentialXMLPath)

			if(targetEnv==null ||  targetEnv.isEmpty() || confidentialXMLPath ==null ||  confidentialXMLPath.isEmpty()) {
				

				print "Target environment or confidentialXMLPath is missing :"+targetEnv +"confidentialXMLPath : "+confidentialXMLPath;
			}

			configXML.envPaths.env.find { it.'@name'.equalsIgnoreCase(targetEnv) }.envPath.each { path ->
				path.each { attr ->
					envPath = attr.toString();
					println "envPath :"+envPath;
					if(envPath==null ||(envPath!=null && envPath.isEmpty())) {
						throw new Exception("Environment path not found");
					}
				}

			}
			configXML.CVS.env.find { it.'@name'.equalsIgnoreCase(targetEnv) }.targetFile.each { targetFile ->
				
				binding = [:]
				
				targetFile.placeHolder.each { placeHolder ->										
										
							def placeHolderKey	= placeHolder.placeHolderKey.text();
							def placeHolderValue 	= placeHolder.placeHolderValue.text();
							println "Replacing placeHolder :"+placeHolderKey;
							binding.put(placeHolderKey, placeHolderValue);
					
						}

				def tempTargetFilePath = targetFile.targetFilePath.text();
				targetFilePath = envPath+File.separator +tempTargetFilePath.toString();
				println "targetFilePath :"+targetFilePath;
				tempTargetFile = new File(targetFilePath);

				file = new File(targetFilePath)			
				def engine = new groovy.text.XmlTemplateEngine() 		
				def template = engine.createTemplate(tempTargetFile.text).make(binding)		
				def modifiedXML = template.toString();
				modifiedXML = modifiedXML.replaceAll('>\\s[!\\s]*', '>').replaceAll('[!\\s]*\\s</', '</')
				File modifiedFile = new File(targetFilePath)					
				modifiedFile.write XmlUtil.serialize(modifiedXML)
				print "secrets injection done for file -> ${targetFilePath}\n"

			} // targetFile


		} catch (Exception e) {

			print "Exception occured while injecting the password :"+e.printStackTrace()
			System.exit(1)

		}
